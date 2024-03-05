#! /usr/bin/env sh

target_dir="$1"


variant_set="--variants regular italic 200 400 500 600 800"

# https://stackoverflow.com/questions/11002820/why-should-we-include-ttf-eot-woff-svg-in-a-font-face
formats="--formats woff2 woff"
# woff eot svg

install_set(){
    if [ -n "$target_dir" ]; then
        export target_dir="$target_dir"
    fi

    ./install-font.sh $@ $variant_set $formats
}

# Monospace fonts
#https://fonts.google.com/specimen/Roboto+Mono?classification=Monospace

install_set \
roboto-mono \
ubuntu-mono \
noto-sans-mono \
cuisine \
cutive-mono \
azeret-mono \
nova-mono


# handwriting fonts

#unifrakturmaguntia: latin medieval
#yesteryear: slanted and not continuous calligraphy with little dynamics
#ruthie: like a pen drawing (like concept art in progress)
#pacifico thick lines with non existant edges (only! swung and nothing else)
#caveat: block hand writing
#courgette: block hand writing, but warped lines and no edges

install_set \
kalam \
merienda \
yesteryear \
unifrakturmaguntia \
ruthie \
pacifico \
caveat \
courgette

# slab serif -> blocky serifs (usually horizontal serifs)
install_set \
cutive \
josefin-slab \
roboto-slab \
rokkitt

# sans-serif fonts (not additional serifs -> good readability)

#roboto: clean, aprupt and straight endings, nothing fancy but looks quite clean @ regular weight

install_set \
roboto \
protest-riot \
protest-revolution \
open-sans \
lato \
inter \
noto-sans \
raleway \
nunito \
quicksand \
manrope \
josefin-sans \
cabin \
hind-siliguri \
mukta \
mulish \
jost \
m-plus-rounded-1c \
red-hat-display \
merriweather-sans \
source-sans-3 \
abeezee \
philosopher \
amaranth \
atkinson-hyperlegible \
alef \
Comfortaa \


# serif font (more legible than handwriting font and less than sansserif fonts -> good for headings, as they are big anyway and therefore
# provide enough legibility and adding a bit of stylization via serifs)

#merriweather: simple and clean - subtle serifs
#noto-serif: readable but a bit slabby blocky
#libre-baskerville: triangular like serifs, well swung lines, but a bit sharp
#bree: rounded look - thick bottom serifs (-> only use for accents)
#spectral: swung and dynamic, small very sharp serifs
#marcellus: almost non existant serifs, thick line accents during char paths
#crimson-pro: quite rounded chars and serifs
#quattrocento: sharp minimal serifs on bottom and tow, swung/round char shapes
#gelasio: somewhat blocky, round, chars and serifs -> very good legibility
#courier-prime: almost mono space, simple non dynamic lines, strongly rounded serifs, minimal
#stix-two-text: newspaper print like, a bit like times new roman but a bit more in the direction of sansserifs - pointy, slightly dynamic lines, clean
#literata: strange looks a bit like a block structure, but at the same time swung (with almost to perfect circles and sways) -> very geometrical
#vidaloka: squeezed look (horizontally), thin horizontal lines, parrallel serifs, blobby circular end serifs
#yeseva-one: looks a bit like hebrew glyphs, extreme dynamic in lines width, one side of char very thick the other very thin, semi defined serifs -> point to top bottom, or the horizontal parallel serifs
# -> kinda bad legibility, but looks cool/ancient
# castoro: swung a bit sans like, swung on the bottom and pointy on the top
#amita: almost handwriting like, but better structures -> depending on the characters extremely unlegible ('r' and 's' characters mix really badly) -> for accents
#lustria: straight lines (almost at a grid), very subtle line dynamics, subtle serifs, parallel serifs
#suez-one: very thick, geometrical, many straight lines unless swung required
#ovo: swung, subtle serifs, lines ends in roundings, designerish look
#young-serif: slanted! serifs and lines, thick look, some dynamics between top and bottom, a bit little distance between letters on bottom serifs, good constrast between swung and straight
#gabriela: esoteric, serifs and line ends are swung in at the ends, handwriting or brush looks with dynamics
#asul: dynamic in double V shape, trapez, minimal serifs, subtle angled dynamics, quite sans like
#montaga: slanted swings in lines, uneven base shapes, slanted serifs at all tops
#Comfortaa: rounded glyph edges, very clean and minimal (maybe a bit too minimal -> harder to read than other sans-serif fonts)

./install-font.sh \
merriweather \
noto-serif \
libre-baskerville \
bree-serif \
spectral \
marcellus \
unna \
crimson-pro \
quattrocento \
gelasio \
courier-prime \
stix-two-text \
literata \
vidaloka \
yeseva-one \
libre-caslon-text \
lusitana \
castoro \
amita \
lustria \
suez-one \
ovo \
young-serif \
radley \
gabriela \
asul \
montaga \
bona-nova \
milonga \
kaisei-harunoumi

#caudex \

#montaga -> ugly in bold@600
