import os
import ast
import sys
import json
import uuid
import base64
import zipfile
import requests
import importlib.util
from  pathlib import Path

from truffle.common import get_logger
from truffle.cli.color_argparse import ColorArgParser
from truffle.platform.sdk_pb2 import AppUploadProgress
from truffle.runtime import HOST, RuntimeType

logger = get_logger()


def get_png_dimensions(file_path):
    with open(file_path, "rb") as f:
        signature = f.read(8)  
        if signature != b"\x89PNG\r\n\x1a\n":
            raise ValueError("Not a valid PNG file: " + file_path)
        f.read(4) 
        if f.read(4) != b"IHDR":
            raise ValueError("Invalid PNG structure: header not found in " + file_path)

        width = int.from_bytes(f.read(4), "big")
        height = int.from_bytes(f.read(4), "big")
        return width, height


def default_mainpy(proj_name : str) -> str:
    return str(r"""
import truffle
import requests

class PROJECT_NAME:
    def __init__(self):
        self.client = truffle.TruffleClient() # the client for using the SDK API, will be a global in next release
                                            # this allows you to perform LLM inference, text embeddings, ask the user for input, etc.
        self.notepad = "" # you can store state in your class, and it will be saved between tool calls and by the backend to reload saved tasks
    @truffle.tool(
        description="Replace this with a description of the tool.",
        icon="brain" # these are Apple SF Symbols, will be fontawesome icon names in next release, https://fontawesome.com/search?o=r&ic=free&ip=classic
    )
    @truffle.args(user_input="A description of the argument") #you can add descriptions to your arguments to help the model!
    def PROJECT_NAMETool(self, user_input: str) -> dict[str, str]: # You have to type annotate all arguments and the return type
        def do_something(user_input):
            pass
        do_something(user_input) # you can do whatever you want in your tools, just make sure to return a value!
                                # add any imports you need at the top of the file and to the requirements.txt and they will be automatically installed
        return { "response" : "Hello, world!" }# all tools must return a value, and take at least one argument

    @truffle.tool("Adds two numbers together", icon="plus-minus")
    def Calculate(self, a: int, b: int) -> list[int]:
        return [a, b, a + b] 
    
    @truffle.tool("Returns a joke", icon="face-smile")
    def GetJoke(self, num_jokes : int) -> str:
        num_jokes = 1 if num_jokes < 1 else num_jokes # support for constraints on arguments is coming soon! 
        response = requests.get(f"https://v2.jokeapi.dev/joke/Programming,Misc?format=txt&amount={num_jokes}")
        if response.status_code != 200:
            print("JokeAPI returned an error: ", response.status_code) # any logs from your app are forwarded to the client
            raise ValueError("JokeAPI is down, try again later")   # any exceptions you raise are sent to the model automatically as well
        return response.content
    
    
    # an example of tools using state! you might want to use this to store things like API keys, or user preferences
    @truffle.tool("Take notes", icon="pencil")
    def TakeNote(self, note: str) -> str:
        self.notepad += note + "\n"
        return "Added note.\n Current notes: \n" + str(self.notepad)

    @truffle.tool("Read notes", icon="glasses")
    @truffle.args(clear_after="whether to clear notes after reading.")
    def ReadNotes(self, clear_after: bool) -> str:
        notes = self.notepad
        if clear_after is True:
            self.notepad = ""
        return "Current notes: \n" + str(notes)
        
    @truffle.tool("Searches with Perplexity", icon="magnifying-glass")
    @truffle.args(query="The search query")
    def PerplexitySearch(self, query: str) -> str:    
        self.client.tool_update("Searching perplexity...") # send an update to the client, will be displayed in the UI if version supports it
        return self.client.perplexity_search(query=query, model="sonar-pro") # SDK API provides free access to Perplexity
    
    # you can add as many tools as you want to your app, just make sure they are all in the same class, and have the @truffle.tool decorator
    # of course, you may also add any other methods you want to your class, they will not be exposed to the model but can be used in your tools
    # any files in your project directory will be included in the bundle, so you can use them in your tools as well, use relative paths from main.py
        

if __name__ == "__main__":
    truffle.run(PROJECT_NAME())
""").replace("PROJECT_NAME", proj_name)


def get_client_userdata_dir() -> Path:
    import sys, os #move this when moving to sdk
    #replicate electron app.getPath('UserData') behavior
    if sys.platform == "win32":
        base = os.getenv("APPDATA", os.path.expanduser("~\\AppData\\Roaming"))
    elif sys.platform == "darwin":
        base = os.path.expanduser("~/Library/Application Support")
    else:
        base = os.getenv("XDG_CONFIG_HOME", os.path.expanduser("~/.config"))
    CLIENT_DIR_NAME = "TruffleOS-Development" if os.getenv("TRUFFLE_DEV") else "TruffleOS" # ie. ~/Library/Application\ Support/truffle-os - userdata/clientname
    userdata = Path(os.path.join(base, CLIENT_DIR_NAME))
    if not userdata.exists():
        raise ValueError(f"User data directory {userdata} does not exist")
    if not userdata.is_dir():
        raise ValueError(f"User data directory {userdata} is not a directory")
    return userdata


def get_user_id() -> str:
    if os.getenv("TRUFFLE_CLIENT_ID"):
        return os.getenv("TRUFFLE_CLIENT_ID")
    try:
        userdata = get_client_userdata_dir()
        user_id_path = userdata / "magic-number.txt"
        if not user_id_path.exists():
            raise ValueError(f"Magic Number file @{user_id_path} does not exist")
        with open(user_id_path, 'r') as f:
            user_id = f.read().strip()
        if not user_id or len(user_id) < 6:
            raise ValueError(f"Magic Number file @{user_id_path} is empty/too short {len(user_id)}")
        
        if not user_id.isdigit():
            raise ValueError(f"Magic Number file @{user_id_path} is not a number")
        if user_id == "1234567891":
            raise ValueError(f"Magic Number file @{user_id_path} is the placeholder number")
        return user_id
    except Exception as e:
        print(f"Error getting user ID: {e}")
        raise


def get_base_url() -> str:
    url = "https://overcast.itsalltruffles.com:2087" if not os.getenv("TRUFFLE_DEV") else "https://forecast.itsalltruffles.com:2087" 
    try:
       path = get_client_userdata_dir()
       url_file = path / "current-url"
       if url_file.exists():
            with open(url_file, "r") as f:
                url_file_contents = f.read().strip()
                if url_file_contents:
                    url = url_file_contents
                    print(f"Using URL from file: {url}")
    except Exception as e:
        logger.error(f"Error getting base URL fron client: {str(e)}")
    print(f"Using URL-  {url}")
    return url


def post_zip_and_log_sse(url : str, zip_path : Path, user_id : str) -> bool:
    headers = {
        'user_id': user_id,
    }
    assert zip_path.exists(), f"path {zip_path} does not exist"
    assert zip_path.is_file(), f"path {zip_path} is not a file"
    assert zip_path.suffix == '.truffle', f"zip_path {zip_path} is not a truffle file"
    with open(zip_path, 'rb') as f:
        files = { 
            'file': ( zip_path.stem, f, 'application/zip'),
        }

        with requests.post(url + "/install", headers=headers, files=files, stream=True, timeout=10) as resp:
            if resp.status_code != 200:
                raise requests.exceptions.HTTPError(f"Error: {resp.status_code} {resp.text}")

            # TODO, progress bar?
            buffer = bytes()
            for line_bytes in resp.iter_lines(decode_unicode=False, chunk_size=1024):
                line = line_bytes.decode('utf-8', errors='replace')
                logger.debug(f"decode line: ''{line}''")
                if not line:
                    if buffer:
                        try: #deserialize the event
                            event_bytes = buffer
                            prog = AppUploadProgress()

                            decoded = base64.b64decode(event_bytes)
                            while decoded.endswith(b'\0'): #remove excessive trailing null bytes (semi hack- makes it more robust)
                                decoded = decoded[:-1] 
                            
                            prog.ParseFromString(decoded)

                            logger.debug(prog)
                            
                            if prog.substep:
                                logger.info(f"{prog.substep}")
                            #update upload status code goes here 
                            #right now status updates are implemented just enough

                            if prog.HasField("error"):
                                logger.error(f"Error: {prog.error}")

                            if prog.step == AppUploadProgress.UploadStep.STEP_INSTALLED: return True

                            
                        #long logs still might cause a parsing error, i will fix this later when i improve the logs themselves 

                        except Exception as e:  # so expect these errors will occur 
                            #- assume you can keep reading on past the occasional bad msg until the connection closes/ network errors happen
                            # FIXME, just hiding for now
                            # logger.error(f"Error parsing event pb: {e}")
                            logger.debug(f"buffer: <<<\n{buffer}\n>>>\n") #buffer might be large and ugly
                            logger.debug(f"line: <<<\n{buffer.decode('utf-8',errors='replace')}\n>>>\n") #line might be large and ugly
                        buffer = bytes() 
                    continue
                
                if line.startswith('data:'):
                    buffer += line_bytes[5:].lstrip() #this is not a great way to parse this but for sake of example - dont copy paste it 
                #basic SSE format is data: <data> \n\n (so \n\n delimiter and data: prefix)
    return False


def upload(path: Path):
    if not path.exists():
        logger.error(f"Path {path} does not exist - cannot upload")
        sys.exit(1)
    
    if path.is_dir():
        truffle_files = [f for f in os.listdir(path) if f.endswith('.truffle')]
        if not truffle_files:
            logger.error("No .truffle file found in the directory")
            sys.exit(1)
        if len(truffle_files) > 1:
            logger.error("Multiple .truffle files found in the directory")
            sys.exit(1)
        path = path / truffle_files[0]
    elif path.is_file():
        if not path.suffix == '.truffle':
            logger.error("File does not have a .truffle extension")
            sys.exit(1)
        if not zipfile.is_zipfile(path):
            logger.error("File is not a valid zip archive")
            sys.exit(1)
    else:
        logger.error("Path is neither a directory nor a file") # is this possible?
        sys.exit(1)
    
    logger.info(f"Uploading project: {path}")

    URL = get_base_url()
    user_id = get_user_id()
    logger.debug(f"Uploading to {URL} with user ID {user_id}")

    try:
        if(post_zip_and_log_sse(URL, path, user_id)):
            logger.success("Upload successful - check your client for installation errors and confirmation")
            sys.exit(0)
        else:
            logger.error("Upload failed - please try again")
            sys.exit(1)
    except Exception as e:
        logger.error(f"Upload failed: unknown error: {e}")
        sys.exit(1)


APP_FILES = [
    "manifest.json",
    "requirements.txt",
    "main.py",
    "icon.png",
]


def init_project(project : Path):
    if project.exists() and not project.is_dir():
            logger.error(f"Path {project} exists and is not a directory, cannot init")
            sys.exit(1)
    
    def alphanum_camel(string: str) -> str:
        return ''.join(w.capitalize() for w in string.split() if w.isalnum())

    def get_input(prompt : str, default : str = None, field : str = 'Input'):
        has_default = default is not None and len(default) > 0
        txt = logger.input(f"{prompt}: ") if not has_default else logger.input(f"{prompt} ({default}): ")
        if len(txt) > 0:
            return txt
        elif len(txt) == 0 and has_default:
            return default
        else:
            logger.error(f"{field} cannot be empty!")
            return get_input(prompt, default)
    
    logger.info("Provide some information about your project: ")
    proj_name = get_input(f"Name for your app", project.name, "App name")
    proj_desc = get_input("Description for your app", "Does app things", "App description")
    example_prompts = []
    logger.info("(optional) Provide some example prompts for your app: ")
    logger.info("These will be used for the automatic app selection feature, and can be edited in the manifest.json post-init")
    while True:
        msg = "Enter an example prompt for your app (or leave empty to finish): " if len(example_prompts) == 0 else "Enter another example prompt for your app (or leave empty to finish): "
        ex = logger.input(msg)
        if len(ex) == 0: break
        example_prompts.append(ex)
    
    print('')

    # If user runs in non empty dir, create a file with project name in CamelCase, increment number if dir exists
    # else if the dir is empty or doesn't exist then create the files there
    if project.exists() and any(project.iterdir()):
        for i in range(999):
            new_path = Path(project / (alphanum_camel(proj_name)+(str(i) if i>0 else '')))
            if not new_path.exists():
                project = new_path
                break
            i += 1
    project.mkdir(parents=True)

    for f in APP_FILES:
        if f == "icon.png":
            try:
                c = requests.get("https://pngimg.com/d/question_mark_PNG68.png")
                if c.status_code != 200: raise requests.HTTPError(c.status_code)
                with open(project / f, "wb") as icon: icon.write(c.content)
            except Exception as e:
                logger.error(f"Failed to download and create default icon: {e}")
                logger.warning("Creating a placeholder icon, please change it manually")
                (project / f).touch()
            logger.debug(f"-> Created default icon.png")
        elif f == "manifest.json":
            manifest = {
                "name": proj_name,
                "description": proj_desc,
                "example_prompts": example_prompts,
                "packages": [],
                "manifest_version": 1,
                "app_bundle_id" : str(uuid.uuid4()) # we can't just find your app by name, we need a unique identifier in case you change it! 
            }
            with open(project / f, "w") as mani:
                mani.write(json.dumps(manifest, indent=4, sort_keys=False, ensure_ascii=False))
            logger.debug(f"-> Created manifest.json with:\n {manifest}")
        elif f == "requirements.txt":
            with open(project / f, "w") as reqs: reqs.write("requests\n")
            logger.debug(f"-> Created requirements.txt")
        elif f == "main.py":
            class_name = alphanum_camel(proj_name)
            with open(project / f, "w") as main: main.write(default_mainpy(class_name))
            logger.debug(f"-> Created main.py with default content")
        else:
            (project / f).touch()

    logger.success(f"Initialized project in {project.resolve()}")
    logger.info(f"You can now build your project with 'truffle build {project.relative_to(Path.cwd())}', and upload it with 'truffle upload {project.relative_to(Path.cwd())}'")
    sys.exit(0)


def build(builddir: Path):
    if not builddir.exists():
        logger.error(f"Path {builddir} does not exist - cannot build")
        sys.exit(1)
    if not builddir.is_dir():
        logger.error("Path is not a directory, please provide a directory to build")
        sys.exit(1)

    def check_file(p : Path):
        name = p.name
        if name == "manifest.json":
            manifest = json.loads(p.read_text())
            required_keys = [
                'name', 'description', 'app_bundle_id', 'manifest_version'
            ]
            for key in required_keys:
                if key not in manifest:
                    logger.error(f"Missing key {key} in manifest.json")
                    sys.exit(1)
            if 'developer_id' not in manifest:
                manifest['developer_id'] = get_user_id()
            if 'example_prompts' not in manifest or len(manifest['example_prompts']) == 0:
                logger.warning("No example prompts found in manifest.json, auto-selection performance may be poor")
        elif name == "requirements.txt":
            reqs = p.read_text().strip().split("\n")
            if len(reqs) == 0:
                logger.error("Empty/unparseable requirements.txt file")
                sys.exit(1)
            banned_reqs = ["truffle", "grpcio", "protobuf"]
            for r in reqs:
                for banned in banned_reqs:
                    if r.find(banned) != -1:
                        logger.error(f"Do not include {banned} in requirements.txt")
                        sys.exit(1)
                logger.debug(f"-> found requirement '{r}' - OK")
        elif name == "main.py":
            main_text = p.read_text()
            if main_text.find("import truffle") == -1:
                logger.error("Missing import truffle in main.py")
                sys.exit(1)
            
            if main_text.find("truffle.run") == -1:
                logger.error("Missing truffle.run call in main.py")
                sys.exit(1)
            
            if main_text.find("class") == -1:
                logger.error("Missing class definition in main.py")
                sys.exit(1)
            
        elif name == "icon.png":
            try:
                w, h = get_png_dimensions(p)
                ICON_SIZE = 512
                if w != 512 or h != 512:
                    logger.error(f"Invalid icon.png size: {w}x{h} - must be {ICON_SIZE}x{ICON_SIZE}")
                    sys.exit(1)
            except Exception as e:
                logger.error(f"Invalid icon.png file: {e}")
                sys.exit(1)
        else:
            logger.error(f"Unknown file: {p}")
            sys.exit(1)
        logger.debug(f"Checked {p} - OK")


    def must_exist(p : Path):
        if not p.exists() or not p.is_file():
            logger.error(f"Missing file: {p} - invalid project")
            sys.exit(1)
        if p.stat().st_size == 0:
            logger.error(f"Empty file: {p} - invalid project")
            if p.name == "requirements.txt":
                logger.warning("if a requirements.txt file is not needed, please remove it")
            sys.exit(1)
        check_file(p)

    for f in APP_FILES:
        must_exist(builddir / f)

    for file in builddir.iterdir():
        try:
            if file.is_file() and not file.name.endswith(".truffle"):
                size = file.stat().st_size
                if size > (1024 * 1024 * 10): 
                    logger.error(f"Unexpectedly large file {file}, did you mean to include this?")
                    sys.exit(1)
        except Exception as e:
            continue
    
    main_path = builddir / "main.py"
    tree = ast.parse(main_path.read_text())

    inst_code = None
    for node in ast.walk(tree):
        if isinstance(node, ast.Call):
            func = node.func
            if (
                isinstance(func, ast.Attribute) and
                func.attr == "run" and
                isinstance(func.value, ast.Name) and
                func.value.id == "truffle"
            ):
                inst_code = ast.get_source_segment(main_path.read_text(), node)
                break

    if not inst_code:
        logger.error("Unable to find truffle.run(...) in main.py")
        sys.exit(1)

    spec = importlib.util.spec_from_file_location("main", str(main_path))
    main_mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(main_mod)
    if HOST in [RuntimeType.DEV, RuntimeType.TRUFFLE]:
        logger.warning("Skipping public runtime checks, run again with TRUFFLE_RUNTIME='CLIENT' to run them")
    else:
        eval(inst_code, main_mod.__dict__)
        # ^ this run TruffleClientRuntime.build 

    def make_zip(src_dir: Path, dst_file: Path):
        assert src_dir.exists() and src_dir.is_dir(), f"Invalid source directory: {src_dir}"
        assert dst_file.suffix == ".truffle", f"Invalid destination file: {dst_file}"
        with zipfile.ZipFile(dst_file, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, _, files in os.walk(src_dir):
                for file in files:
                    if file.endswith('.truffle') or file == '.DS_Store':
                        continue
                    file_path = os.path.join(root, file)
                    arcname = os.path.relpath(file_path, src_dir)
                    zipf.write(file_path, arcname)
        return dst_file

    bundle = make_zip(builddir, builddir / f"{builddir.name}.truffle")
    logger.success(f"Built project {builddir.name} to {bundle.relative_to(Path.cwd())}")
    logger.info(f"Upload with 'truffle upload {builddir.relative_to(Path.cwd())}'")
    sys.exit(0)


def cli():
    parser = ColorArgParser(prog="truffle", description="Truffle SDK CLI")
    subparsers = parser.add_subparsers(dest="action", description="the CLI action: upload / init / or build", required=True, help="The action to perform")
    
    def add_subcommand(name: str, help: str):
        p = subparsers.add_parser(name, help=help)
        p.add_argument("path", help="The path to the project", nargs="?", default=os.getcwd())
    
    actions = {
         "upload" : {"help": "Upload the project to the cloud", "fn": upload},
         "init" : {"help": "Initialize a new project", "fn": init_project},
         "build" : {"help": "Build the project", "fn": build},
    }

    for name, args in actions.items():
        add_subcommand(name, args["help"])

    args = parser.parse_args()
    if not args.action or args.action not in actions:
        parser.print_help()
        logger.error(f"\t-> please provide one of the following actions: {', '.join(actions.keys())}")
        sys.exit(1)
    
    cmd = actions[args.action]
    cmd["fn"](Path(args.path).resolve()) # resolve fixes . as an arg
    

def main():
    cli()

if __name__ == "__main__":
    main()
