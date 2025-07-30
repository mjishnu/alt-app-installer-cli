import asyncio
import datetime
import html
import json
import os
import platform
import re
import warnings
from xml.dom import minidom

import aiohttp

warnings.filterwarnings("ignore")
script_dir = os.path.dirname(os.path.abspath(__file__))


def os_arc():
    machine = platform.machine().lower()

    if machine.endswith("arm64"):
        return "arm64"
    if machine.endswith("64"):
        return "x64"
    if machine.endswith("32") or machine.endswith("86"):
        return "x86"
    else:
        return "arm"


# cleans My.name.1.2 -> myname
def clean_name(badname):
    name = "".join(
        [(i if (64 < ord(i) < 91 or 96 < ord(i) < 123) else "") for i in badname]
    )
    return name.lower()


def select_best(items, curr_arch, ignore_ver=False, is_installer=False):
    """
    Select best item based on scoring system.
    For UWP: Prioritize arch -> file type -> date -> version
    For installers: Prioritize arch -> locale -> installer type
    """

    def score(item):
        if is_installer:
            arch, locale, inst_type, url = item
            # 2 = exact arch, 1 = neutral, 0 = other
            arch_score = 2 if arch == curr_arch else (1 if arch == "neutral" else 0)
            # 2 = en-us, 1 = en/us contained, 0 = other
            locale_score = (
                2
                if locale == "en-us"
                else 1
                if ("en" in locale or "us" in locale)
                else 0
            )
            return (arch_score, locale_score, inst_type)
        else:
            arch, ext, modified_str, version_str = item
            fav_type = {"appx", "msix", "msixbundle", "appxbundle"}
            arch_score = 2 if arch == curr_arch else (1 if arch == "neutral" else 0)
            type_score = 1 if ext in fav_type else 0

            if ignore_ver:
                dt = 0
                ver_tuple = (0, 0, 0, 0)
            else:
                clean_str = modified_str.rstrip("Z")
                clean_str = re.sub(r"(\.\d{6})\d+", r"\1", clean_str)
                dt = datetime.datetime.fromisoformat(clean_str)
                ver_tuple = tuple(map(int, version_str.split(".")))
            return (arch_score, type_score, dt, ver_tuple)

    # Filter arch to (curr_arch or "neutral"), else fallback
    candidates = [item for item in items if item[0] in (curr_arch, "neutral")]
    candidates = candidates or items

    return max(candidates, key=score)


def parse_dict(main_dict, file_name, ignore_ver, all_dependencies):
    """Parse the dictionary and return the best file(s)"""
    # Prep the incoming 'file_name' for matching
    base_name = clean_name(file_name.split("-")[0])
    blockmap_pattern = re.compile(r".+\.BlockMap")

    # Build a dictionary of structured data for easy lookup
    full_data = {}
    for key, value in main_dict.items():
        if not blockmap_pattern.search(str(key)):
            parts = key.split("_")
            mapped_key = (
                clean_name(parts[0]),
                parts[2].lower(),
                parts[-1].split(".")[1].lower(),
                value,
                parts[1],
            )
            full_data[mapped_key] = key

    # Collect entries by their “cleaned-up name”
    names_dict = {}
    for mapped_key in full_data:
        name_base = mapped_key[0]
        names_dict.setdefault(name_base, []).append(mapped_key[1:])

    file_arch = None
    main_file_name_entry = None
    pat_main = re.compile(base_name)
    sys_arch = os_arc()

    # Identify the main file
    matching_base = None
    for name_base in names_dict:
        if pat_main.search(name_base):
            matching_base = name_base
            break

    # Process matching entry if found
    if matching_base:
        content_list = names_dict[matching_base]
        arch, ext, modified, version = select_best(content_list, sys_arch)
        main_file_name_entry = full_data[(matching_base, arch, ext, modified, version)]
        file_arch = sys_arch if arch == "neutral" else arch
        del names_dict[matching_base]
    else:
        raise Exception("No file found")

    # Gather dependencies or single-file results
    final_list = []
    for name_base, content_list in names_dict.items():
        if all_dependencies:
            for data in content_list:
                final_list.append(full_data[(name_base, *data)])
        else:
            arch, ext, modified, version = select_best(
                content_list, file_arch, ignore_ver
            )
            final_list.append(full_data[(name_base, arch, ext, modified, version)])

    # If we found a main file, append it
    if main_file_name_entry:
        final_list.append(main_file_name_entry)
        file_name = main_file_name_entry
    else:
        # If no explicit main file found, pick the first from final_list
        if final_list:
            file_name = final_list[0]

    return final_list, file_name


async def uwp_gen(session, data_list, ignore_ver, all_dependencies):
    """Get UWP app installer info from Microsoft Store"""
    cat_id = data_list["WuCategoryId"]
    main_file_name = data_list["PackageFamilyName"].split("_")[0]
    release_type = "retail"

    # 1. Get encrypted cookie
    with open(f"{script_dir}/data/xml/GetCookie.xml", "r") as f:
        cookie_template = f.read()

    response_text = await (
        await session.post(
            "https://fe3cr.delivery.mp.microsoft.com/ClientWebService/client.asmx",
            data=cookie_template,
            headers={"Content-Type": "application/soap+xml; charset=utf-8"},
        )
    ).text()

    cookie_doc = minidom.parseString(response_text)
    cookie = cookie_doc.getElementsByTagName("EncryptedData")[0].firstChild.nodeValue

    # 2. Request IDs and filenames
    with open(f"{script_dir}/data/xml/WUIDRequest.xml", "r") as f:
        wuid_template = f.read().format(cookie, cat_id, release_type)

    response_text = await (
        await session.post(
            "https://fe3cr.delivery.mp.microsoft.com/ClientWebService/client.asmx",
            data=wuid_template,
            headers={"Content-Type": "application/soap+xml; charset=utf-8"},
        )
    ).text()

    xml_doc = minidom.parseString(html.unescape(response_text))

    # Collect filenames {ID: (prefixed_filename, modifiedDate)}
    filenames_map = {}
    for files_node in xml_doc.getElementsByTagName("Files"):
        try:
            node_id = files_node.parentNode.parentNode.getElementsByTagName("ID")[
                0
            ].firstChild.nodeValue
            prefix = files_node.firstChild.attributes[
                "InstallerSpecificIdentifier"
            ].value
            fname = files_node.firstChild.attributes["FileName"].value
            modified = files_node.firstChild.attributes["Modified"].value
            filenames_map[node_id] = (f"{prefix}_{fname}", modified)
        except KeyError:
            continue

    if not filenames_map:
        raise Exception("server returned an empty list")

    # 3. Parse update IDs from SecuredFragment
    identities = {}
    name_modified = {}
    for fragment_node in xml_doc.getElementsByTagName("SecuredFragment"):
        try:
            fn_id = fragment_node.parentNode.parentNode.parentNode.getElementsByTagName(
                "ID"
            )[0].firstChild.nodeValue
            file_name, modified = filenames_map[fn_id]
            top_node = fragment_node.parentNode.parentNode.firstChild
            update_id = top_node.attributes["UpdateID"].value
            rev_num = top_node.attributes["RevisionNumber"].value

            name_modified[file_name] = modified
            identities[file_name] = (update_id, rev_num)
        except KeyError:
            continue

    # 4. Choose the best files via parse_dict
    parse_names, main_file_name = parse_dict(
        name_modified, main_file_name, ignore_ver, all_dependencies
    )

    # Build a dict of {filename: (update_id, revision_number)}
    final_dict = {}
    for val in parse_names:
        final_dict[val] = identities[val]

    # 5. Download URLs for each selected file
    with open(f"{script_dir}/data/xml/FE3FileUrl.xml", "r") as f:
        file_template = f.read()

    file_dict = {}

    async def geturl(update_id, revision_num, file_name):
        resp_text = await (
            await session.post(
                "https://fe3cr.delivery.mp.microsoft.com/ClientWebService/client.asmx/secured",
                data=file_template.format(update_id, revision_num, release_type),
                headers={"Content-Type": "application/soap+xml; charset=utf-8"},
            )
        ).text()
        doc = minidom.parseString(resp_text)
        for loc in doc.getElementsByTagName("FileLocation"):
            url = loc.getElementsByTagName("Url")[0].firstChild.nodeValue
            # blockmap vs actual file
            if len(url) != 99:
                file_dict[file_name] = url

    tasks = []
    for file_name, (upd_id, rev_num) in final_dict.items():
        tasks.append(asyncio.create_task(geturl(upd_id, rev_num, file_name)))

    await asyncio.gather(*tasks)

    # 6. Verify everything downloaded
    if len(file_dict) != len(final_dict):
        raise Exception("server returned an incomplete list")

    return file_dict, parse_names, main_file_name, True


async def non_uwp_gen(session, product_id):
    """Get non-UWP app installer info from Microsoft Store"""

    # 1. Fetch package manifest
    api_url = (
        f"https://storeedgefd.dsx.mp.microsoft.com/v9.0/packageManifests/{product_id}"
    )
    api_params = "?market=US&locale=en-us&deviceFamily=Windows.Desktop"

    response = await session.get(api_url + api_params)
    data = json.loads(await response.text())

    if not data.get("Data"):
        raise Exception("Server returned empty package data")

    # 2. Get package name and installers
    package_name = data["Data"]["Versions"][0]["DefaultLocale"]["PackageName"]
    installers = data["Data"]["Versions"][0]["Installers"]

    # 3. Extract unique installer combinations
    installer_options = {
        (i["Architecture"], i["InstallerLocale"], i["InstallerType"], i["InstallerUrl"])
        for i in installers
    }

    # 5. Build result
    chosen = select_best(installer_options, curr_arch=os_arc(), is_installer=True)
    main_file_name = f"{clean_name(package_name)}.{chosen[2]}"

    return (
        {main_file_name: chosen[3]},  # file_dict
        [main_file_name],  # file list
        main_file_name,  # main file
        False,  # is_uwp flag
    )


def extract_product_id(url):
    """Extract product ID from Microsoft Store URL"""
    pattern = re.compile(r".+\/([^\/\?]+)(?:\?|$)")
    if match := pattern.search(str(url)):
        return match.group(1)
    raise ValueError("Invalid URL format - Please provide a valid Microsoft Store URL")


async def fetch_product_details(session, product_id):
    """Fetch product details from Microsoft Store API"""
    api_url = f"https://storeedgefd.dsx.mp.microsoft.com/v9.0/products/{product_id}"
    params = "?market=US&locale=en-us&deviceFamily=Windows.Desktop"

    async with session.get(api_url + params) as response:
        data = await response.text()
        return json.loads(
            data,
            object_hook=lambda obj: {
                k: json.loads(v) if k == "FulfillmentData" else v
                for k, v in obj.items()
            },
        )


async def url_generator(url, ignore_ver, all_dependencies):
    """Generate download URLs for Microsoft Store apps"""
    try:
        product_id = extract_product_id(url)

        timeout = aiohttp.ClientTimeout(total=60)
        async with aiohttp.ClientSession(
            timeout=timeout, raise_for_status=True
        ) as session:
            response = await fetch_product_details(session, product_id)

            if not response.get("Payload"):
                raise ValueError("Invalid product ID or URL")

            # Get fulfillment data from response
            data_list = response["Payload"]["Skus"][0].get("FulfillmentData")

            # Route to appropriate handler based on app type
            if data_list:
                return await uwp_gen(session, data_list, ignore_ver, all_dependencies)
            return await non_uwp_gen(session, product_id)

    except (aiohttp.ClientError, json.JSONDecodeError) as e:
        raise ConnectionError(f"Failed to fetch app details: {str(e)}")
