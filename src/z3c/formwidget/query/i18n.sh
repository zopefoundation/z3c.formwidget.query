#!/bin/bash
BASEFOLDER=$PWD

# This function parses the strings to be translated in folder
# for a certain domain
function i18nizer {
    FOLDERS=$1
    DOMAIN=$2

    POT=$BASEFOLDER/locales/$DOMAIN.pot
    MANUAL_POT=$BASEFOLDER/locales/$DOMAIN-manual.pot
    touch $POT $MANUAL_POT

    i18ndude rebuild-pot --pot $POT --create $DOMAIN $FOLDERS
    i18ndude merge --pot $POT --merge $MANUAL_POT

    for LANG in $BASEFOLDER/locales/*/LC_MESSAGES; do
        PO_BASENAME=$LANG/$DOMAIN
        touch $PO_BASENAME.po
        i18ndude sync --pot $POT $PO_BASENAME.po
        msgfmt -o $PO_BASENAME.mo $PO_BASENAME.po
    done
}

i18nizer $BASEFOLDER 'z3c.formwidget.query'

grep -R fuzzy locales/ -A2
