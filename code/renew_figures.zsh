#!/bin/zsh

setopt extended_glob

# (>&2 echo "Converting svg to pdf..")

codedir="$(dirname $0:A)"
rootdir="$codedir/.."

checksums="$rootdir/svg-hashes.log"
touch "$checksums"

cd "$rootdir/fig"


################################################
# avoid updating svg files that did not change #
################################################

get_svg_sha() {
    # the 16MB svg is too much over NFS and not needed anyway
    sha512sum *.svg | grep -v spikey_photo\\.svg
}

# svg files that changed
to_update=$(diff \
    --unchanged-line-format= --old-line-format= --new-line-format='%L' \
    "$checksums" =(get_svg_sha) | sed -e 's:^[0-9a-f]*\s*::')

echo $to_update | while read -r f; do
    if [[ -n "$f" ]]; then
        echo "Converting $f -> ${f:r}.pdf"
        inkscape "--export-pdf=${f:r}.pdf" --export-dpi=600 "$f"
    fi
done

get_svg_sha > $checksums



# for i in {schematic_recurrent_bm,schematic_syn_delay,schematic_deep_network};
# do
#     convert -density 300 $i.pdf -quality 100 $i.png
# done


######################
# update mpl figures #
######################

cd "$codedir"

python -m mpl_figures plot_all

cd "$rootdir/fig"
pdflatex -shell-escape figHWfull.tex
rm figHWfull.log
rm figHWfull.aux
pdflatex -shell-escape figTHfull.tex
rm figTHfull.log
rm figTHfull.aux
pdflatex -shell-escape figSetupFull.tex
rm figSetupFull.log
rm figSetupFull.aux