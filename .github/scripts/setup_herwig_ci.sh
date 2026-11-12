# Source after the Key4hep setup, from the CTest build directory.
# Some Key4hep builds omit ThePEG's nested lib directory from Herwig's search path.
herwig_binary=$(command -v Herwig)
herwig_links=$(ldd "$herwig_binary")
thepeg_soname=$(awk '$1 ~ /^libThePEG\.so\./ && $3 == "not" {print $1; exit}' <<< "$herwig_links")
if [[ -n "$thepeg_soname" ]]; then
    # Look alongside the selected Herwig package in the active CVMFS stack.
    herwig_package=$(dirname "$(dirname "$(realpath "$herwig_binary")")")
    packages_dir=$(dirname "$herwig_package")
    stack_dir=$(dirname "$packages_dir")
    thepeg_libraries=()
    for candidate in "$stack_dir"/thepeg/*/lib/ThePEG/"$thepeg_soname" \
                     "$packages_dir"/thepeg-*/lib/ThePEG/"$thepeg_soname"; do
        if [[ -f "$candidate" ]]; then
            thepeg_libraries+=("$candidate")
        fi
    done
    if [[ ${#thepeg_libraries[@]} -ne 1 ]]; then
        printf 'Expected one %s alongside Herwig in %s, found %s\n' \
            "$thepeg_soname" "$herwig_package" "${#thepeg_libraries[@]}" >&2
        return 1
    fi
    thepeg_libdir=$(dirname "${thepeg_libraries[0]}")
    export LD_LIBRARY_PATH="$thepeg_libdir${LD_LIBRARY_PATH:+:$LD_LIBRARY_PATH}"
fi

# Herwig loads these defaults even for the electron–positron steering.
pdf_dir="$PWD/herwig-pdf"
for pdf_set in CT14lo CT14nlo; do
    mkdir -p "$pdf_dir/$pdf_set"
    for pdf_file in "$pdf_set.info" "${pdf_set}_0000.dat"; do
        curl -fsSL --retry 3 "https://lhapdfsets.web.cern.ch/current/$pdf_set/$pdf_file" \
            -o "$pdf_dir/$pdf_set/$pdf_file"
    done
done
export LHAPDF_DATA_PATH="$pdf_dir${LHAPDF_DATA_PATH:+:$LHAPDF_DATA_PATH}"
