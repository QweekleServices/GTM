# Changelog

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
