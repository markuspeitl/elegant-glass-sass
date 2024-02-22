#! /usr/bin/env sh

font_to_install="$1"

if [ -z "$font_to_install" ]; then  
    python3 "$script_dir/download-fonts.py" --all --all_file ./all_google_fonts_list.json --list
fi

fonts_to_install_and_args=$@

#echo "$fonts_to_install"

script_dir=$(dirname "$0")

if [ -z "$target_dir" ]; then
    target_dir="$script_dir/.."
fi

echo "Downloading fonts $fonts_to_install_and_args"
python3 "$script_dir/download-fonts.py" --css_file "$target_dir/fonts.scss" --fonts_dir "$target_dir/fonts" "$fonts_to_install_and_args"


#./install-font.sh montserrat poppins lato protest-strike dancing-script protest-guerilla protest-revolution eb-garamont prompt lobster --variants 200 400 600 800
#./install-font.sh montserrat raleway --variants 200 400 600 800



