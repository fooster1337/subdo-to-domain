import argparse
import tldextract
import sys
import os
from colorama import Fore, init
if os.name == 'nt':
    init()

# color code
blue = Fore.BLUE
reset = Fore.RESET
green = Fore.GREEN


class std:
    def __init__(self, params=None) -> None:
        self.params = params

    # convert domain on params to subdomain
    def convert(self, domain):
        ex = tldextract.extract(domain).domain + '.' + tldextract.extract(domain).suffix
        if self.params["--add-http"]:
            ex = "http://"+ex
        if self.params["--add-https"]:
            ex = "https://"+ex
        if self.params["--add-www"]:
            if ex.startswith("http://"):
                ex = ex.replace("http://", "http://www.")
            elif ex.startswith("https://"):
                ex = ex.replace("https://", "https://www.")
        if self.params["--only-tld"]:
            if any(s in tldextract.extract(domain).suffix for s in self.params["--only-tld"]):
                return ex
        else:
            return ex
    
    def start(self):
        if not self.params:
            print("Params argument cannot None."); sys.exit(0)
        domain = self.params["domain"]
        result = [self.convert(i) for i in domain if self.convert(i)]
        if result:
            if not self.params["--silent"]:
                print(f"{len(result)} Domain has been converted...")
        else:
            print(f"No result.. Exiting"); sys.exit(0)
        # save file
        with open(self.params["--output"], "w+", encoding="utf8") as f:
            if self.params["--rm-duplicate"]:
                f.write('\n'.join(list(dict.fromkeys(result))))
            else:
                f.write('\n'.join(result))
        f.close()

        if not self.params["--silent"]:
            print("All result has been save to {}".format(self.params["--output"]))
        sys.exit(0)
        
def print_usage(program_name):
    usage = f"""Subdomain To Main Domain Converter Tools. (https://github.com/fooster1337)
usage : python {program_name} <sitename/filename> <argument>\n
AVAILABLE ARGUMENTS
 -h, --help                      Show help messages
 -o, --output filename           Save result into file (default={green}extract_result.txt{reset})
 -d, --only-tld tld1,tld2,tld3   Filter only you give is saved (example = -d go,edu,gov)
 --add-http                      Add http into result (Disable if --add-https True)
 --add-https                     Add https into result
 --add-www                       Add www into result 
 --rm-duplicate                  Remove duplicate URL
 --silent                        Silent when proccess"""
    print(usage)

def main():
    if len(sys.argv) <= 1 or '-h' in sys.argv or '--help' in sys.argv:
        print_usage(sys.argv[0])
        sys.exit(0)

    parser = argparse.ArgumentParser()
    parser.add_argument('domain')
    parser.add_argument('-o', '--output', required=False, default="extract_result.txt")
    parser.add_argument('-d', '--only-tld', required=False)
    parser.add_argument('--add-http', action='store_true', default=False, required=False)
    parser.add_argument('--add-https', action='store_true', default=False, required=False)
    parser.add_argument('--add-www', action='store_true', default=False, required=False)
    parser.add_argument('--rm-http', action='store_true', default=False, required=False)
    parser.add_argument('--rm-https', action='store_true', default=False, required=False)
    parser.add_argument('--rm-www', action='store_true', default=False, required=False)
    parser.add_argument('--rm-duplicate', action='store_true', default=False, required=False)
    parser.add_argument('--silent', action='store_true', default=False, required=False)
    args = parser.parse_args()
    
    # default params 
    params = {
        "--only-tld": [],
        "--output": "extract_result.txt",
        "--add-http": False,
        "--add-https": False,
        "--add-www": False,
        "--rm-https": False,
        "--rm-http": False,
        "--rm-www": False,
        "--rm-duplicate": False,
        "--silent": False
    }
    
    
    
    # detect if file or domain
    try:
        # read file and split into list
        params["domain"] = open(args.domain, 'r', encoding='utf8').read().splitlines()
    except Exception as e: 
        params["domain"] = args.domain.split()
        

    # check output arg 
    if args.output:
        params['--output'] = args.output

    if args.only_tld:
        for tld in args.only_tld.split(','):
            params['--only-tld'].append(tld)
    
    if args.add_http and args.add_https:
        print("Conflict beetwen --add-http and --add-https. --add-http features will be off")
        params['--add-https'] = True

    elif args.add_http:
        params['--add-http'] = True
    
    if args.add_https:
        params['--add-https'] = True

    if args.add_www:
        params['--add-www'] = True

    if args.rm_duplicate:
        params['--rm-duplicate'] = True
    if args.silent:
        params['--silent'] = True

    if not params["--silent"]:
        print(f"Start proccessing {len(params['domain'])}")
    # start the fucking program
    std(params=params).start()

if __name__ == '__main__':
    main()


