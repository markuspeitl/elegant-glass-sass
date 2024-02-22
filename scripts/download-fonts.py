#! /usr/bin/env python3


import io
import zipfile
import argparse
import json
import os
import pathlib
from subprocess import Popen
import subprocess
import sys
# pip3 install requests
import requests


# curl http://fonts.googleapis.com/css?family=Raleway |


# list all tracked fonts sorted by popularity
# curl https://gwfh.mranftl.com/api/fonts > /tmp/fonts-list.txt && micro /tmp/fonts-list.txt


# curl "https://gwfh.mranftl.com/api/fonts/raleway?subsets=latin,latin-ext"


# curl -o raleway.zip "https://gwfh.mranftl.com/api/fonts/raleway?download=zip&subsets=latin,latin-ext&variants=regular,bold&formats=woff"
# unzip raleway.zip
# rm raleway.zip

# curl "https://gwfh.mranftl.com/api/fonts/raleway?download=zip&subsets=latin,latin-ext&variants=regular,700&formats=woff" | busybox unzip -


# https://github.com/majodev/google-webfonts-helper
# target_url="https://gwfh.mranftl.com/api/fonts"


import argparse
from typing import Any, Literal

default_target_url = "https://gwfh.mranftl.com/api/fonts"
default_all_fonts_file_path = '/tmp/fonts-list.txt'


def get_joined_or_empty(array_to_join: list, join_token: str = ',') -> str | Literal['']:
    if (not array_to_join):
        return ""

    return join_token.join(array_to_join)


def get_font_target_url_from_cfg(font_target_id: str, config: dict[str, Any] = {}) -> str:

    if (config.get('all', None)):
        return config.get('all')

    url = config.get('url', None)
    font_id = font_target_id

    subsets = config.get('subsets', None)
    variants = config.get('variants', None)
    formats = config.get('formats', None)

    param_options = [
        "subsets=" + get_joined_or_empty(subsets),
        "variants=" + get_joined_or_empty(variants),
        "formats=" + get_joined_or_empty(formats),
    ]

    param_options_string = "&".join(param_options)

    download_url = f"{url}/{font_id}?{param_options_string}"

    print(f"Target download url: {download_url}")

    return download_url


def get_download_url_from_cfg(font_target_id: str, config: dict[str, Any] = {}) -> str:
    down_operation_option = "download=zip"

    # & and ? format can be invalid -> because i am not handling empty values
    download_url = f"{get_font_target_url_from_cfg(font_target_id, config)}&{down_operation_option}"

    return download_url


def get_remote_json(url: str):
    get_result = requests.get(url=url, params=None)
    result_list_json = get_result.json()
    return result_list_json


def print_get_remote_json(url: str, indent: int = 4) -> Any:
    result_list_json = get_remote_json(url)

    if (indent < 0):
        indent = None

    formatted_result_string = json.dumps(result_list_json, indent=indent)

    print(formatted_result_string)

    return result_list_json

# def family_and_variant_from_file_name()


def get_file_name_from_info(font_info, selected_variant_info, file_type: str = None) -> str:

    remote_font_id = font_info['id']
    remote_font_version = font_info['version']
    remote_store_id = font_info['storeID']

    remote_variants_list = font_info['variants']

    variant_id = selected_variant_info['id']

    no_ext_name = f"{remote_font_id}-{remote_font_version}-{remote_store_id}-{variant_id}"

    if (not file_type):
        return no_ext_name

    return f"{no_ext_name}.{file_type}"


"""
#https://css-tricks.com/snippets/css/using-font-face-in-css/
@font-face {
  font-family: 'MyWebFont';
  src: url('webfont.eot'); /* IE9 Compat Modes */
  src: url('webfont.eot?#iefix') format('embedded-opentype'), /* IE6-IE8 */
       url('webfont.woff2') format('woff2'), /* Super Modern Browsers */
       url('webfont.woff') format('woff'), /* Pretty Modern Browsers */
       url('webfont.ttf')  format('truetype'), /* Safari, Android, iOS */
       url('webfont.svg#svgFontName') format('svg'); /* Legacy iOS */
}
"""


def generic_font_url(variant_file_name, fonts_dir_from_css, extension, format=None):
    if (not format):
        format = extension

    return f"url('{fonts_dir_from_css}/{variant_file_name}.{extension}') format('{format}')"


def get_font_format_src_options(variant_file_name, fonts_dir_from_css, extension, format=None):
    if (not format):
        format = extension

    font_file_from_css = f"{fonts_dir_from_css}/{variant_file_name}.{extension}"
    return font_file_from_css, format


def get_font_format_src_options_fn(extension, format=None):
    return lambda variant_file_name, fonts_dir_from_css: get_font_format_src_options(variant_file_name, fonts_dir_from_css, extension, format)

# def get_generic_font_url_fn(extension, format=None):
#    return lambda variant_file_name, fonts_dir_from_css: generic_font_url(variant_file_name, fonts_dir_from_css, extension, format)

# def get_generic_font_url_format_fn(extension, font_format):
#    return lambda variant_file_name, fonts_dir_from_css: generic_font_url(variant_file_name, fonts_dir_from_css, extension, font_format)


formats_mapper_dict = {
    'woff': get_font_format_src_options_fn('woff'),
    'woff2': get_font_format_src_options_fn('woff2'),
    'eot': get_font_format_src_options_fn('eot', 'embedded-opentype'),
    'svg': get_font_format_src_options_fn('svg'),
    'tiff': get_font_format_src_options_fn('tiff', 'truetype'),
}
formats_mapper_dict['truetype'] = formats_mapper_dict['tiff']


"""def get_font_face_for_variant_formats(selected_formats, font_dir, css_path) -> str:

    font_id = font_info['id']
    # font_family = font_id
    font_family = font_info['family']
    font_weight = selected_variant_info['fontWeight']
    font_style = selected_variant_info['fontStyle']
"""


def get_font_face_for_variant(font_info, selected_variant_info, font_dir, css_path) -> str:

    # font_family = 'raleway-regular'
    # fonts_dir_from_css = "../fonts"
    # font_dir_path_obj = pathlib.PurePath(font_dir)
    css_path_obj = pathlib.PurePath(css_path)
    fonts_dir_from_css = os.path.relpath(font_dir, css_path_obj.parent)

    remote_font_id = font_info['id']
    font_family = remote_font_id

    # remote_font_version = font_info['version']
    # remote_store_id = font_info['storeID']
    # remote_variants_list = font_info['variants']

    print(selected_variant_info)
    # formats are stored flat in the dict: 'woff': 'val'
    # variant_formats = selected_variant_info.keys()

    variant_file_name = get_file_name_from_info(font_info, selected_variant_info)

    valid_format_urls = []

    for registered_format in formats_mapper_dict:
        if (registered_format in selected_variant_info):
            var_format_path, var_format_type = formats_mapper_dict[registered_format](variant_file_name, fonts_dir_from_css)

            format_file_path = pathlib.Path(os.path.join(css_path_obj.parent, var_format_path)).resolve()
            print(format_file_path)

            if (format_file_path and os.path.exists(format_file_path)):

                font_url_entry = f"url('{var_format_path}') format('{var_format_type}')"
                valid_format_urls.append(font_url_entry)

            else:
                print(f"Format {registered_format} is not registered for variant -> skipping")

    print(valid_format_urls)

    if (not valid_format_urls or len(valid_format_urls) <= 0):
        return None

    css_font_face_src_content = ',\n\t\t'.join(valid_format_urls)

    font_weight = selected_variant_info['fontWeight']
    font_style = selected_variant_info['fontStyle']

    font_face_lines = [
        f"\n",
        "@font-face {",
        f"\tfont-family: '{font_family}';",
        f"\tfont-weight: {font_weight};",
        f"\tfont-style: {font_style};",
        f"\tsrc:",
        f"\t\t{css_font_face_src_content};",
        "}",
    ]

    return "\n".join(font_face_lines)


stripped_css_faces_cache: str | None = None


def append_font_face_to_css(css_font_face_string, target_css_append_path):
    global stripped_css_faces_cache

    if (not os.path.exists(target_css_append_path)):
        return None

    if (stripped_css_faces_cache):
        stripped_css_content = stripped_css_faces_cache

    if (not stripped_css_faces_cache):
        with open(target_css_append_path, 'r') as css_file:
            css_content = css_file.read()
            # Remove all whitespace
            stripped_css_content = ''.join(css_content.split())

            stripped_css_faces_cache = stripped_css_content

    with open(target_css_append_path, 'a+') as css_file:
        if css_font_face_string:
            # print(css_font_face)

            stripped_css_font_face = ''.join(css_font_face_string.split())

            if (not stripped_css_font_face in stripped_css_content):
                css_file.write(css_font_face_string)

                stripped_css_faces_cache += stripped_css_font_face
                print(css_font_face_string)
            else:
                print("font face exists in file -> skipping")


def get_css_target_path(config) -> str:

    target_dir = config.get('fonts_dir', None)
    if (not target_dir):
        target_dir = os.getcwd()

    target_css_append_path = config.get('css_file', None)

    if (not target_css_append_path):
        target_css_append_dir_path = config.get('css_dir', None)

        if (target_css_append_dir_path):
            target_css_append_path = os.path.join(target_css_append_dir_path, 'fonts.css')

    if (not target_css_append_path):
        target_css_append_path = os.path.join(target_dir, 'fonts.css')

    if (not os.path.exists(target_css_append_path)):
        target_css_path_obj = pathlib.PurePath(target_css_append_path)
        target_css_append_path = os.path.join(target_css_path_obj.parent, target_css_path_obj.stem + ".scss")

    return target_css_append_path


def list_all_fonts(config: dict[str, Any] = {}):
    if (config.get('all', None)):

        url = config.get('url', default_target_url)
        print(f"Listing all remote fonts from endpoint: {url}")

        result_fonts_list_file = config.get('all_file', default_all_fonts_file_path)
        print(f"Target file: {result_fonts_list_file}")

        if (os.path.exists(result_fonts_list_file)):
            print(f'font list file at {result_fonts_list_file} does already exist -> please remove to redownload update')
            return

        result_list_json = print_get_remote_json(url)

        formatted_result_string = json.dumps(result_list_json, indent=4)

        print(formatted_result_string)

        with open(result_fonts_list_file, 'a+') as file:
            file.write(formatted_result_string)

        return


def list_selected_font_info(font_target_id: str, config: dict[str, Any] = {}):
    if (config.get('list', False)):

        print(f"Listing info for font: {font_target_id}")

        url = get_font_target_url_from_cfg(font_target_id, config)

        print(f"Font request url: {url}")

        result_list_json = print_get_remote_json(url)
        return


def download_font_variant_format(font_format, base_font_info, font_variant_info, fonts_target_dir, overwrite_existing=False):

    if (font_format not in font_variant_info):
        print(f"Can not download: {font_format} does not exist for variant")
        return None

    font_format_url = font_variant_info[font_format]

    target_file_name = get_file_name_from_info(base_font_info, font_variant_info, font_format)
    target_file_path = os.path.join(fonts_target_dir, target_file_name)

    if (os.path.exists(target_file_path) and not overwrite_existing):
        print(f"SKIP Download: Font face format at: {target_file_path} already exists and overwriting is disabled")
        return font_format

    downloaded_font = requests.get(url=font_format_url, stream=True)

    # font_data_io = io.BytesIO(downloaded_font.content)

    print("Writing font to:")
    print(target_file_path)

    with open(target_file_path, "wb") as font_file:
        font_file.write(downloaded_font.content)

    return font_format


def download_variant_get_fontface(base_font_info, font_variant_info, fonts_target_dir, target_css_append_path, requested_variants: list[str], requested_formats: list[str], overwrite_existing=False):

    print(f"download_variant_get_fontface: {str(font_variant_info)}")

    variant_id = font_variant_info['id']

    if (variant_id in requested_variants):

        downloaded_variant_font_formats = list(map(lambda requested_format: download_font_variant_format(requested_format, base_font_info, font_variant_info, fonts_target_dir, overwrite_existing=overwrite_existing), requested_formats))

        font_face_css_string = get_font_face_for_variant(base_font_info, font_variant_info, fonts_target_dir, target_css_append_path)

        print("Downloaded variant formats: ")
        print(downloaded_variant_font_formats)

        """for key in font_variant_info:

            downloaded_variant_font_formats = list(map(lambda requested_format: download_font_variant_format(requested_format, base_font_info, font_variant_info, fonts_target_dir, overwrite_existing=overwrite_existing), requested_formats))
        """

        return font_face_css_string


def download_font_add_font_face(font_target_id, fonts_target_dir, target_css_append_path, config: dict[str, Any] = {}):
    print(f"download_font_add_font_face {font_target_id} - {fonts_target_dir} - {target_css_append_path}")

    current_font_target_dir = os.path.join(fonts_target_dir, font_target_id)

    if (not os.path.exists(current_font_target_dir)):
        os.makedirs(current_font_target_dir)

    font_target_url = get_font_target_url_from_cfg(font_target_id, config)
    font_info = get_remote_json(font_target_url)

    remote_font_id = font_info['id']
    remote_font_version = font_info['version']
    remote_store_id = font_info['storeID']
    remote_variants_list = font_info['variants']

    variant_css_font_face_strings = []

    print(f"Processing remote detected font variants: {str(remote_variants_list)}")

    for remote_variant_info in remote_variants_list:
        config_variants = config.get('variants', [])
        config_formats = config.get('formats', [])
        overwrite = config.get('overwrite', False)

        font_face_css_string = download_variant_get_fontface(font_info, remote_variant_info, current_font_target_dir, target_css_append_path, config_variants, config_formats, overwrite_existing=overwrite)
        if (font_face_css_string):
            variant_css_font_face_strings.append(font_face_css_string)

    for css_font_face in variant_css_font_face_strings:
        append_font_face_to_css(css_font_face, target_css_append_path)


def list_or_download_font_and_add_css(font_target_id, fonts_target_dir, target_css_append_path, config: dict[str, Any] = {}):

    print(f"list_or_download_font_and_add_css: {font_target_id}")

    if (config.get('list', False)):
        return list_selected_font_info(font_target_id, config)

    return download_font_add_font_face(font_target_id, fonts_target_dir, target_css_append_path, config)


def download_google_webfont(config: dict[str, Any] = {}):
    # print('Calling download_google_webfont')

    font_target_ids = config.get('font_target_ids', [])

    if (config.get('all', None)):
        return list_all_fonts(config)

    fonts_target_dir = config.get('fonts_dir', None)
    if (not fonts_target_dir):
        fonts_target_dir = os.getcwd()

    target_css_append_path = get_css_target_path(config)

    for font_target_id in font_target_ids:

        print(f"Processing target font {font_target_id}")
        list_or_download_font_and_add_css(font_target_id, fonts_target_dir, target_css_append_path, config)

    """down_url = get_download_url_from_cfg(config)

    target_dir = config.get('fonts_dir', None)
    if (not target_dir):
        target_dir = os.getcwd()

    download_response = requests.get(down_url, stream=True)

    # zip_file_bytes = download_response.content
    zip_file_bytes = io.BytesIO(download_response.content)
    # zip_file_bytes = download_response.raw

    files_in_archive = []

    with zipfile.ZipFile(zip_file_bytes, 'r') as zip_file:
        files_in_archive = zip_file.namelist()
        zip_file.extractall(target_dir)

    print("Extracted files: ")
    print(files_in_archive)"""

    """down_unzip_cmd = f"curl \"{down_url}\" | busybox unzip -"

    down_unzip_cmd_args = [
        "curl",
        f"\"{down_url}\"",
        "|",
        "busybox",
        "unzip",
        "-"
    ]

    print(" ".join(down_unzip_cmd_args))

    down_unzip_cmd = " ".join(down_unzip_cmd_args)

    # down_unzip_cmd_args[1] = " ".join(down_unzip_cmd_args[1:])

    cwd = os.getcwd()
    abs_target_dir = os.path.abspath(target_dir)
    os.system(f"cd {abs_target_dir} && {down_unzip_cmd} && cd {cwd}")

    # download_process: subprocess.Popen = subprocess.Popen(down_unzip_cmd_args, cwd=target_dir)
    # download_process.wait()"""


def get_current_file_dir() -> str:

    return pathlib.PurePath(__file__).parent


def add_font_download_parsing_options(parser: argparse.ArgumentParser):
    parser.add_argument('font_target_ids', nargs='*', help="")
    parser.add_argument('-a', '--all', action="store_true", help="List all fonts and write a file with the result to this path")
    parser.add_argument('-af', '--all_file', help="List all fonts and write a file with the result to this path", default=default_all_fonts_file_path)
    parser.add_argument('-l', '-ls', '--list', action="store_true", help="Do not download font -> print infos instead")

    # parser.add_argument('-d', '-dd', '--download_dir', help="Download to the passed dir", default=get_current_file_dir())
    parser.add_argument('-c', '-css', '--css_file', help="Path of the css file to append the font face to")

    parser.add_argument('-fd', '-font_d', '--fonts_dir', help="Download the fonts into this dir - should be the desired font dir")  # , default=get_current_file_dir())
    parser.add_argument('-cd', '-css_d', '--css_dir', help="Target the font.css in this dir for defining the font faces linking to the downloaded fonts")  # , default=get_current_file_dir())

    parser.add_argument('-w', '--overwrite', action="store_true", help="Overwrite existing fonts on disk with the same name")

    parser.add_argument('-u', '-url', '--url', action="store_true", help="Target url to send the get requests to", default=default_target_url)

    parser.add_argument('-f', '--formats', nargs='+', help="Which font formats to download -> adding/removing formats to existing css fontface is not supported", choices=['woff', 'woff2', 'svg', 'ttf', 'local', 'eot'], default=['woff2', 'woff', 'eot', 'svg'])
    parser.add_argument('-s', '--subsets', nargs='+', help="Which font subsets to download", choices=['latin', 'latin-ext', "devanagari", "greek", "cyrillic-ext", "cyrillic", "greek-ext", "vietnamese"], default=['latin', 'latin-ext'])
    parser.add_argument('-v', '--variants', nargs='+', help="Which font variants to download. examples: 300, 300italic, regular, italic, 600, 600italic, 700, 700italic, 800, 800italic", default=['200', '400', '600', '800'])


# Example:
# python3 download-fonts.py raleway -s latin latin-ext -v regular 400 -f woff2 eot
# python3 download-fonts.py raleway --list
# python3 download-fonts.py "" --all

def main(parser: argparse.ArgumentParser | None = None):
    parser_description = "Wrapper for open google webfonts downloading service "

    if (not parser):
        parser = argparse.ArgumentParser(
            description=parser_description
        )
        add_font_download_parsing_options(parser)

    args: argparse.Namespace = parser.parse_args()

    config: dict[str, Any] = vars(args)

    variants = config.get('variants', [])

    for i in range(0, len(variants)):
        # Ugly hack to enable requesting the 400 variant, as it is usually has the 'regular' id
        if ('400' in variants[i]):
            variants[i] = variants[i].replace('400', 'regular')

    download_google_webfont(config)


if __name__ == '__main__':
    sys.exit(main())
