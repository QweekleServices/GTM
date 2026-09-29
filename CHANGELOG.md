# Changelog

## 1.2.0 - 29/09/2026
 - Nouveau déclencheur `Qweekle - CE - Relance apres consentement` (Base, GA4, Meta, Google Ads) sur `qweekle_consent_update`, `cookie_consent_update`, `axeptio_update`, `didomi-consent` et, à défaut, `page_view`. Les balises d'arrivée (`[GA4] Configuration`, `[Google Ads] Configuration`, `[Google Ads] Conversion Linker`, `[Meta] Pixel Base + PageView`) se déclenchent aussi sur ce déclencheur, une fois par page. Sur la Vente en ligne (SPA), un nouveau visiteur qui acceptait les cookies après le chargement n'était pas mesuré à l'arrivée : `gclid`, `utm_*` et `fbclid` étaient perdus
 - Fonction commune `qweekleUpdateConsent()` : pousse l'événement `qweekle_consent_update` après la mise à jour du consentement
 - Tag `Consent Mode - Default` : déclenché sur « Initialisation du consentement - Toutes les pages » au lieu de All Pages. Il reste un filet de sécurité : en HTML personnalisé, ses commandes ne sont traitées qu'après le chargement du conteneur
 - README : relance des balises après consentement (3.1.1, 4.1, 5.1, 6.x, checklist, dépannage), procédure de mise à jour depuis une version précédente
 - README : le template GTM de la CMP doit être sur « Initialisation du consentement », avec un consentement par défaut « refusé ». Constaté en test : un template CookieYes réglé par défaut sur « accordé » laissait partir les balises avant le choix du visiteur
 - tools/validate.py : vérification du déclencheur de relance, des balises d'arrivée et du déclenchement du tag Default

## 1.1.0 - 18/09/2026
 - Tag `Consent Mode - CMP Update` : refonte autour d'une fonction commune `qweekleUpdateConsent()`, ajout du bloc CookieYes (4 CMP couvertes)
 - Consent Mode : priorite du tag Default remontee a 100 — il se declenchait APRES le tag CMP Update, ce qui pouvait ecraser le consentement mis a jour par la CMP
 - Tag CMP : bannieres de bloc sorties des commentaires — decommenter un bloc en suivant le README ne casse plus le tag
 - Bloc CookieYes : gestion des payloads `accepted` en chaine de caracteres, de la liste vide, et non-modification du consentement si le format est inconnu
 - Ajout de `tools/validate.py` (verification des 4 modules, de la procedure de decommentage et de la synchro README/JSON)
 - DATALAYER-REFERENCE : ajout de l'événement `sign_out`, section « Validation terrain » basée sur une capture Tag Assistant réelle
 - README : documentation des 4 blocs CMP, avertissement sur la double mise à jour du consentement
 - README : exclusion du domaine de paiement des referents GA4 documentee dans le parcours normal (section 3.2, checklist, depannage) et plus seulement dans la bascule demo -> live
 - README : nouvelle section 4.6 « Utilisation d'un compte démo » (bascule démo → live, mise à jour des URL dans GTM)
 - DATALAYER-REFERENCE : `add_payment_info` confirmé en conditions réelles (dernière étape de tunnel mesurable côté marchand)

## 1.0.0 - 02/07/2026
 - Initial version
