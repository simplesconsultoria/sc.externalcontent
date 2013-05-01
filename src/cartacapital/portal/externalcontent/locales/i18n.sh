#! /bin/sh
# see http://maurits.vanrees.org/weblog/archive/2010/10/i18n-plone-4 for more information

I18NDOMAIN="cartacapital.portal.externalcontent"
# find the source, as it shoul be in the src directory
SOURCE=`find . -type d | grep -m 1 "src/cartacapital/portal/externalcontent"`
LOCALES=`find . -name "locales" -type d | grep "src/cartacapital/portal/externalcontent"`

if [ ! $LOCALES ]; then
    echo "Can't find locales path"
    exit 1
fi

# check if the locales directory is registered
FOUND=`grep -c "i18n:registerTranslations" $SOURCE/configure.zcml`
if [ $FOUND -eq 0 ]; then
    echo "Translations directory 'locales' not registered in your $SOURCE/configure.zcml file"
    exit 1
fi

# rebuild pot file for package's domain and merge it with any manual translations needed
i18ndude rebuild-pot --pot $LOCALES/$I18NDOMAIN.pot --merge $LOCALES/manual.pot --create $I18NDOMAIN $SOURCE

# synchronise translations for package's domain
for po in $LOCALES/*/LC_MESSAGES/$I18NDOMAIN.po; do
    i18ndude sync --pot $LOCALES/$I18NDOMAIN.pot $po
done

# rebuild pot file for Plone's domain
i18ndude rebuild-pot --pot $LOCALES/plone.pot --create plone $SOURCE/configure.zcml $SOURCE/profiles/default

# synchronise translations for Plone's domain
for po in $LOCALES/*/LC_MESSAGES/plone.po; do
    i18ndude sync --pot $LOCALES/plone.pot $po
done
