# Documentation — Modules GTM Qweekle

**Version** : 1.2 — 29/09/2026

**Audience** : clients Qweekle et agences marketing

Pour la référence technique complète du dataLayer, voir [DATALAYER-REFERENCE.md](DATALAYER-REFERENCE.md)

## Téléchargements

Téléchargez les fichiers via clic droit → Enregistrer le lien sous

| Module | Fichier | Lien |
|---|---|---|
| Base *(obligatoire)* | `qweekle-1-base.json` | [Télécharger](https://raw.githubusercontent.com/QweekleServices/GTM/refs/heads/main/qweekle-1-base.json) |
| GA4 | `qweekle-2-ga4.json` | [Télécharger](https://raw.githubusercontent.com/QweekleServices/GTM/refs/heads/main/qweekle-2-ga4.json) |
| Meta | `qweekle-3-meta.json` | [Télécharger](https://raw.githubusercontent.com/QweekleServices/GTM/refs/heads/main/qweekle-3-meta.json) |
| Google Ads | `qweekle-4-ads.json` | [Télécharger](https://raw.githubusercontent.com/QweekleServices/GTM/refs/heads/main/qweekle-4-ads.json) |

---

## Table des matières

1. [Présentation générale](#1-présentation-générale)
2. [Comment importer un module](#2-comment-importer-un-module)
3. [Mise en route minimale](#3-mise-en-route-minimale)
4. [Configurations avancées](#4-configurations-avancées)
5. [Validation et publication](#5-validation-et-publication)
6. [Référence complète des éléments](#6-référence-complète-des-éléments)
7. [Glossaire](#7-glossaire)
8. [Dépannage](#8-dépannage)

---

## 1. Présentation générale

### Ce que ces modules mesurent

Ces modules installent automatiquement le suivi des actions de vos visiteurs sur votre boutique Qweekle. Une fois en place, vous pouvez répondre à des questions concrètes :

- **Combien de visiteurs ont passé une commande ?** → mesuré par GA4 et Google Ads
- **Quels produits sont les plus consultés, ajoutés au panier, achetés ?** → mesuré par GA4 et Meta
- **Mes campagnes publicitaires rapportent-elles de l'argent ?** → mesuré par Google Ads et Meta
- **Qui sont mes clients ?** → mesuré par GA4 (profils, parcours, fidélité)

Chaque module est indépendant : vous n'installez que les plateformes que vous utilisez.

### Comment ça fonctionne — vue d'ensemble

```
┌──────────────────────────────────────────────────────────────────┐
│  SITE QWEEKLE                                                    │
│  Visite · Fiche produit · Ajout panier · Commande…               │
│                         │                                        │
│              pousse des événements dans le                       │
│                         ▼                                        │
│                  [ dataLayer ]                                   │
│            (couche de données invisible)                         │
└─────────────────────────┬────────────────────────────────────────┘
                          │ lu en temps réel
                          ▼
┌──────────────────────────────────────────────────────────────────┐
│  GOOGLE TAG MANAGER (GTM)                                        │
│                                                                  │
│  ┌──────────────────────────────────────────────────────────┐    │
│  │ Module Base — obligatoire                                │    │
│  │ Lit le dataLayer · Vérifie le consentement (RGPD)        │    │
│  └──────────────┬──────────────┬──────────────┬─────────────┘    │
│                 │              │              │                  │
│                 ▼              ▼              ▼                  │
│          ┌──────────┐  ┌──────────┐  ┌──────────────┐           │
│          │  GA4 (2) │  │ Meta (3) │  │  Ads   (4)   │           │
│          └────┬─────┘  └────┬─────┘  └──────┬───────┘           │
└───────────────┼─────────────┼───────────────┼────────────────────┘
                │             │               │
                ▼             ▼               ▼
     ┌──────────────┐ ┌─────────────┐ ┌─────────────────┐
     │   Google     │ │    Meta     │ │   Google Ads    │
     │ Analytics 4  │ │   Pixel     │ │                 │
     │              │ │             │ │                 │
     │ Trafic       │ │ Audiences   │ │ Attribution des │
     │ Ventes       │ │ Conversions │ │ clics publici-  │
     │ Parcours     │ │ Retargeting │ │ taires (ROAS)   │
     └──────────────┘ └─────────────┘ └─────────────────┘
```

Le **dataLayer** est un tableau de données invisible sur votre site, alimenté automatiquement par Qweekle. GTM le lit et redistribue les informations vers les plateformes de votre choix. Vous n'avez rien à coder.

> 💳 **Site de paiement** : le paiement s'effectue sur un domaine dédié qui ne charge pas GTM. Aucune donnée n'est perdue pour autant — la conversion remonte via l'événement `purchase`, émis au retour sur la page de confirmation du site de vente. Il n'y a donc **aucun tag à installer sur le site de paiement**.

### Les 4 modules

```
┌──────────────────────────────────────────────────────────────┐
│                    qweekle-1-base.json                       │
│         Variables DLV · Triggers · Consentement             │
│                       OBLIGATOIRE                            │
└──────────────┬─────────────────┬────────────────────────────┘
               │                 │                │
               ▼                 ▼                ▼
      ┌──────────────┐  ┌──────────────┐  ┌──────────────────┐
      │     GA4      │  │     Meta     │  │   Google Ads     │
      │   (n°2)      │  │   (n°3)      │  │     (n°4)        │
      └──────────────┘  └──────────────┘  └──────────────────┘
        Optionnel          Optionnel           Optionnel
```

**Le module Base est obligatoire.** Il contient les variables de lecture du dataLayer, les déclencheurs partagés entre tous les modules et les variables qui lisent l'état du consentement. Le consentement lui-même est géré par votre CMP, installée dans GTM avec son propre modèle (voir [section 3.1.1](#311-consent-mode--pourquoi-et-comment-configurer)).

**Chaque module optionnel embarque ses propres variables** et les paramètres de consentement sur chaque tag — aucune configuration manuelle du consentement n'est nécessaire après l'import.

**Ordre d'import impératif** : Base en premier, puis les autres dans n'importe quel ordre.

---

## 2. Comment importer un module

La procédure est identique pour les 4 modules.

1. Dans GTM, aller dans **Admin** (roue dentée en haut à droite)
2. Cliquer sur **Importer un container**
3. Sélectionner le fichier `.json` du module
4. Choisir l'espace de travail cible
5. Sélectionner **Fusionner** — ne jamais choisir "Écraser"
6. Cliquer sur **Confirmer**

> ⚠️ **Toujours choisir "Fusionner"**. L'option "Écraser" supprime l'intégralité du container existant et ne peut pas être annulée.

> 📁 Après l'import, les éléments Qweekle sont rangés dans deux dossiers du container — vos propres éléments restent intacts :
> - **`Qweekle - [A CONFIGURER]`** : les seuls éléments que vous devez ouvrir et renseigner (identifiants de plateformes). Tout votre setup se trouve dans ce dossier.
> - **`Qweekle`** : tout le reste (tags, déclencheurs, variables) — préconfiguré, rien à toucher.
>
> Seuls les modèles de la galerie (Facebook Pixel pour le module Meta, GTM Consent State pour tous les modules) et les variables intégrées apparaissent hors dossier, GTM ne permettant pas de les y ranger.

> 💡 **Conseil** : créer un espace de travail dédié avant l'import (GTM → Espaces de travail → `+`) pour pouvoir isoler les changements et les annuler si nécessaire.

> 🔄 **Mise à jour depuis une version précédente** : ré-importez chaque module en choisissant **Fusionner**, puis l'option qui **écrase les éléments en conflit** (et non celle qui les renomme, qui créerait des doublons). Seuls les éléments Qweekle de même nom sont remplacés ; le reste du conteneur n'est pas touché.

---

## 3. Mise en route minimale

Après import, les seules actions requises sont de **renseigner vos identifiants de plateformes** et de **configurer votre bannière cookies**. Tout le reste est préconfiguré.

> 📁 Les variables à renseigner sont regroupées dans le dossier **`Qweekle - [A CONFIGURER]`** du container.
>
> Ce dossier ne couvre en revanche pas tout : la bannière cookies s'installe avec le modèle GTM de votre CMP ([section 3.1.1](#311-consent-mode--pourquoi-et-comment-configurer)), et certaines étapes se passent hors de GTM (activation des Enhanced Conversions, exclusion de référents GA4, validation du domaine Meta).

### 3.1 Module Base — obligatoire pour tous

Aucun identifiant à renseigner. La seule action requise est d'installer votre bannière cookies (CMP) dans GTM, avec son propre modèle.

#### 3.1.1 Consent Mode — pourquoi et comment configurer

**Pourquoi c'est obligatoire** : le RGPD interdit de collecter des données sur les visiteurs européens sans leur accord. Le Consent Mode garantit qu'aucun tag (GA4, Meta, Google Ads) ne se déclenche avant que l'utilisateur ait accepté les cookies. Sans cette configuration, votre client s'expose à des sanctions légales.

**Qui gère le consentement** : votre CMP, installée dans GTM avec le modèle fourni par son éditeur. Ce modèle pose le consentement par défaut avant tout autre événement, puis le met à jour selon le choix du visiteur. Les modules Qweekle ne contiennent aucun tag de consentement : ils lisent simplement cet état.

**Procédure :**

1. GTM → **Tags** → **Nouvelle** → **Configuration de la balise** → **Découvrir d'autres types de balises dans la galerie de modèles de la communauté** → ajoutez le modèle de votre CMP (par exemple « CookieYes CMP », « Cookiebot CMP », ou les modèles d'Axeptio et de Didomi).
2. Renseignez l'identifiant de votre bannière (clé du site, Domain Group ID…).
3. Réglez le **consentement par défaut sur « refusé »** pour l'analyse et la publicité (dans CookieYes : *Default Consent Settings* → toutes les catégories sur *Disabled*, sauf *Necessary*).
4. Activez la transmission des informations de clic dans les URL et l'anonymisation des données publicitaires (*Pass ad click information through URLs* et *Redact ads data* dans CookieYes).
5. Déclencheur : **Initialisation du consentement - Toutes les pages**.
6. Sauvegarder.

> ⚠️ Un modèle réglé par défaut sur « accordé » laisse partir les balises avant le choix du visiteur. Seul le modèle de la CMP, sur « Initialisation du consentement », pose le consentement par défaut à temps : un tag en HTML personnalisé n'est traité qu'après le chargement du conteneur.

> Les balises d'arrivée (GA4, Google Ads, Meta) se déclenchent dès que le visiteur accepte les cookies, grâce aux déclencheurs `Qweekle - CE - Arrivee …`. Ils reconnaissent les événements des modèles Cookiebot, CookieYes, Axeptio et Didomi. Pour une autre CMP, voir [section 4.1](#41-consent-mode--intégration-cmp-détaillée).

---

### 3.2 Module GA4 — mise en route minimale

**Information à récupérer :**

| Information | Où la trouver |
|---|---|
| GA4 Measurement ID | GA4 → Admin → Flux de données → flux web → format `G-XXXXXXXXXX` |

**Action après l'import :**

GTM → **Variables** → ouvrir `Qweekle - CONST - [A CONFIGURER] GA4 Measurement ID` → remplacer `G-XXXXXXXXXX` par l'ID du client.

> Les paramètres de consentement sont déjà configurés sur tous les tags GA4.

**Action obligatoire dans GA4 — exclure le domaine de paiement** ⭐

GA4 → Admin → **Flux de données** → ouvrir le flux web → **Paramètres de balise** → *Afficher plus* → **Répertorier les référents indésirables** → ajouter `payments.qweekle.app` (condition : *Le domaine de référence contient*).

**Pourquoi c'est indispensable** : le paiement se déroule sur un domaine séparé. Au retour sur la page de confirmation, GA4 voit `payments.qweekle.app` comme nouvelle source de trafic et **démarre une nouvelle session**. L'événement `purchase` tombe alors dans cette session, attribué à `payments.qweekle.app / referral` au lieu de la campagne d'origine (Google Ads, Meta, SEO…).

Sans cette exclusion, **100 % des transactions perdent leur source d'acquisition**. Rien n'indique le problème : les achats remontent bien dans GA4, ils sont simplement tous attribués au domaine de paiement — les campagnes payantes semblent ne rien rapporter.

Le module est opérationnel. Pour activer les Conversions améliorées (données utilisateur), voir [section 4.3](#43-enhanced-conversions--ga4).

---

### 3.3 Module Meta — mise en route minimale

**Information à récupérer :**

| Information | Où la trouver |
|---|---|
| Meta Pixel ID | Meta Business Manager → Gestionnaire d'événements → sélectionner le pixel |

**Action après l'import :**

GTM → **Variables** → ouvrir `Qweekle - CONST - [A CONFIGURER] Meta Pixel ID` → remplacer `000000000000000` par l'ID du client.

> Les paramètres de consentement sont déjà configurés sur tous les tags Meta.

Le module est opérationnel.

---

### 3.4 Module Google Ads — mise en route minimale

**Informations à récupérer :**

| Information | Où la trouver |
|---|---|
| Google Ads Conversion ID | Google Ads → Outils → Mesure → Conversions → Tag → format `AW-XXXXXXXXXX` |
| Google Ads Conversion Label | Même endroit, champ "Libellé de conversion" |

**Actions après l'import :**

GTM → **Variables** → ouvrir et renseigner les 2 constantes :
- `Qweekle - CONST - [A CONFIGURER] Google Ads Conversion ID` → `AW-XXXXXXXXXX` du client
- `Qweekle - CONST - [A CONFIGURER] Google Ads Conversion Label` → libellé du client

> Les paramètres de consentement sont déjà configurés sur tous les tags Google Ads.

Le module est opérationnel. Pour configurer le cross-domaine (indispensable si vous avez votre propre nom de domaine), voir [section 4.2](#42-google-ads--conversion-linker-cross-domaine).

---

### ✅ Checklist de setup

Avant de passer à la validation, vérifier que chaque étape est complète.

**Module Base — obligatoire**
- [ ] Module Base importé en mode **Fusion**
- [ ] CMP installée avec son modèle GTM, sur **Initialisation du consentement - Toutes les pages**, avec le consentement par défaut sur **refusé** (analyse et publicité)

**Module GA4** *(si utilisé)*
- [ ] Module GA4 importé en mode **Fusion**
- [ ] `Qweekle - CONST - [A CONFIGURER] GA4 Measurement ID` renseigné
- [ ] `payments.qweekle.app` ajouté aux **référents indésirables** dans GA4 (section 3.2) — sinon toutes les conversions sont attribuées au domaine de paiement

**Module Meta** *(si utilisé)*
- [ ] Module Meta importé en mode **Fusion**
- [ ] `Qweekle - CONST - [A CONFIGURER] Meta Pixel ID` renseigné

**Module Google Ads** *(si utilisé)*
- [ ] Module Google Ads importé en mode **Fusion**
- [ ] `Qweekle - CONST - [A CONFIGURER] Google Ads Conversion ID` renseigné
- [ ] `Qweekle - CONST - [A CONFIGURER] Google Ads Conversion Label` renseigné
- [ ] `Qweekle - CONST - [A CONFIGURER] URL du site de VEL` renseigné
- [ ] `Qweekle - CONST - [A CONFIGURER] URL site vitrine` renseigné *(si site propre)*

**Validation**
- [ ] Mode Aperçu GTM testé (section 5.1)
- [ ] Tags bloqués avant acceptation cookies ✓
- [ ] Première visite testée : balises d'arrivée déclenchées à l'acceptation des cookies (section 5.1) ✓
- [ ] Événement `purchase` vérifié dans chaque plateforme ✓
- [ ] Version publiée dans GTM ✓

---

## 4. Configurations avancées

### 4.1 Consent Mode — intégration CMP détaillée

Le consentement est géré par le modèle GTM de votre CMP (voir [section 3.1.1](#311-consent-mode--pourquoi-et-comment-configurer)). Réglages à vérifier selon la CMP :

| CMP | Modèle GTM | Réglages à vérifier |
|---|---|---|
| CookieYes | « CookieYes CMP » | Website Key ; *Default Consent Settings* sur *Disabled* sauf *Necessary* ; *Pass ad click information through URLs* et *Redact ads data* cochés |
| Cookiebot | « Cookiebot CMP » | Domain Group ID ; consentement par défaut refusé pour *statistics* et *marketing* ; domaine de la Vente en ligne déclaré dans le compte Cookiebot |
| Axeptio | modèle Axeptio | Identifiant du projet ; Consent Mode v2 activé, consentement par défaut refusé |
| Didomi | modèle Didomi | Clé API et identifiant de notice ; Consent Mode activé, consentement par défaut refusé |

Dans tous les cas : déclencheur **Initialisation du consentement - Toutes les pages**, et un seul modèle de CMP dans le conteneur. Déclarez aussi l'adresse de votre Vente en ligne dans le compte de votre CMP.

**Autre CMP** : vérifiez qu'elle propose un modèle GTM compatible Consent Mode v2, et utilisez-le avec les mêmes réglages. Sans modèle, le consentement par défaut ne peut pas être posé à temps.

#### Relance des balises après consentement

Un nouveau visiteur n'a pas encore donné son accord quand la page se charge : les balises d'arrivée (`[GA4] Configuration`, `[Google Ads] Configuration`, `[Google Ads] Conversion Linker`, `[Meta] Pixel Base + PageView`) sont alors bloquées. La Vente en ligne ne rechargeant pas la page à chaque clic, elles ne repartiraient qu'au retour du paiement, sans les paramètres de campagne de l'URL d'arrivée (`gclid`, `utm_*`, `fbclid`).

Les balises d'arrivée ne se déclenchent donc pas sur « All Pages », mais sur deux déclencheurs qui vérifient l'état du consentement à chaque événement :

| Déclencheur | Condition | Balises |
|---|---|---|
| `Qweekle - CE - Arrivee analytics accorde` | `analytics_storage` accordé | `[GA4] Configuration` |
| `Qweekle - CE - Arrivee publicite accordee` | `ad_storage` et `ad_user_data` accordés | `[Google Ads] Configuration`, `[Google Ads] Conversion Linker`, `[Meta] Pixel Base + PageView` |

Chaque balise part **une seule fois par page** : dès le chargement pour un visiteur qui a déjà consenti, au moment de l'acceptation pour un nouveau visiteur, et jamais pour un visiteur qui refuse.

L'état du consentement est lu par les variables `Qweekle - CONSENT - …`, basées sur le modèle de la galerie **GTM Consent State** (Ayudante), importé avec les modules. La condition est portée par les déclencheurs eux-mêmes : dans GTM, une balise « Une fois par page » bloquée par le consentement est considérée comme déjà déclenchée, et ne repartirait pas à l'acceptation.

Les deux déclencheurs écoutent :

| Événement | Poussé par |
|---|---|
| `gtm.js` | GTM, au chargement du conteneur (visiteur ayant déjà consenti) |
| `cookie_consent_update` | Templates GTM Cookiebot et CookieYes |
| `axeptio_update` | Axeptio |
| `didomi-consent` | Didomi |
| `page_view` | Qweekle, à chaque changement de page. Filet de sécurité : la balise part alors à la page suivante, sans les paramètres de campagne |

Si votre CMP pousse un autre événement lors de la mise à jour du consentement, repérez son nom dans l'onglet **Data Layer** du mode Aperçu, puis ajoutez-le à l'expression régulière des deux déclencheurs `Qweekle - CE - Arrivee …` (GTM → **Déclencheurs**).

---

### 4.2 Google Ads — Conversion Linker cross-domaine

Le Conversion Linker est préconfiguré avec `enableCrossDomain: true` et trois variables de domaine. Renseigner celles qui s'appliquent à votre configuration :

| Variable | Valeur par défaut | Quand la renseigner |
|---|---|---|
| `Qweekle - CONST - [A CONFIGURER] URL du site de VEL` | `client.qweekle.shop` | Toujours — remplacer par le vrai domaine du site Qweekle du client |
| `Qweekle - CONST - URL du site de paiement` | `payments.qweekle.app` | Déjà renseignée par défaut — ne pas modifier sauf indication contraire de Qweekle |
| `Qweekle - CONST - [A CONFIGURER] URL site vitrine` | `monsite.fr` | Si votre propre site vitrine redirige vers le tunnel Qweekle |

**Pourquoi c'est important** : sans le troisième domaine (`URL site vitrine`), les clics Google Ads provenant de `monsite.fr` perdent leur GCLID lors du passage vers le domaine Qweekle. La conversion n'est alors pas attribuée à la publicité — le ROAS affiché dans Google Ads est faussé.

Si une variable reste à sa valeur par défaut non pertinente, le Conversion Linker l'ignore simplement.

---

### 4.3 Enhanced Conversions — GA4

Les données utilisateur (email SHA-256, user ID) sont envoyées automatiquement par le tag dès qu'elles sont présentes dans le dataLayer. Pour que GA4 les exploite dans ses rapports, activer les Conversions améliorées côté plateforme :

1. GA4 → Admin → Propriété → **Conversions améliorées**
2. Activer pour le web
3. Sélectionner "Tag Google ou Google Tag Manager"

---

### 4.4 Enhanced Conversions — Google Ads

Les données utilisateur sont envoyées automatiquement sur la conversion Purchase quand elles sont présentes dans le dataLayer. Pour que Google Ads les utilise pour améliorer la précision des conversions :

1. Google Ads → Outils → Mesure → **Conversions** → sélectionner la conversion Purchase
2. Paramètres → **Conversions améliorées** → Activer
3. Choisir "Google Tag Manager"

---

### 4.5 Meta — API Conversions (déduplication)

Si vous utilisez l'API Conversions Meta côté serveur en parallèle du Pixel navigateur, la déduplication est déjà prête. Le tag `[Meta] Purchase` envoie un `order_id` (valeur de `Qweekle - DLV - ecommerce.transaction_id`) qui sert d'`event_id` pour la déduplication entre les hits navigateur et serveur. Aucune configuration supplémentaire dans GTM.

---

### 4.6 Utilisation d'un compte démo

Qweekle peut fournir un **compte de démonstration** pour mettre en place et tester le conteneur GTM avant l'ouverture du site réel. Le dataLayer y est strictement identique à celui d'un compte live : mêmes événements, mêmes champs. Tout ce qui est validé sur la démo fonctionnera à l'identique en production.

**La seule différence est l'URL.** Le compte démo a son propre domaine (par exemple `demo-nom-du-client.qweekle.shop`), distinct de celui du compte live (`client.qweekle.shop`). C'est ce point qui demande quelques ajustements au moment du passage en production.

#### 4.6.1 Passage de la démo au live

**1. Installer la balise GTM sur le compte live**

Renseigner l'identifiant du conteneur (`GTM-XXXXXXX`) dans le back-office Qweekle du **compte live**. Sans cette étape, le site de production n'envoie strictement rien.

**2. Retirer la balise GTM du compte démo** ⭐

Une fois le live en place, supprimer l'identifiant GTM du compte démo. **C'est important** : si les deux comptes utilisent le même conteneur, les tests et démonstrations effectués sur la démo continuent d'envoyer de vrais événements (`purchase` inclus) vers GA4, Meta et Google Ads. Conséquences concrètes :

- du chiffre d'affaires fictif dans les rapports GA4 et Google Ads ;
- des conversions parasites qui faussent le ROAS et polluent l'apprentissage des algorithmes publicitaires ;
- des audiences de remarketing contaminées par des visiteurs de test.

> Si vous devez conserver la démo active en parallèle du live, ne la laissez **pas** pointer vers le conteneur de production : utilisez un second conteneur GTM dédié aux tests, ou filtrez le trafic de démonstration côté GA4 (Admin → Flux de données → définir le trafic interne, puis exclure ce trafic dans les paramètres de données).

**3. Mettre à jour les URL dans GTM**

Le changement de domaine impacte deux endroits du conteneur — voir le détail ci-dessous.

**4. Republier le conteneur**

Les modifications ne prennent effet qu'après un **Envoyer → Publier** (voir [section 5.3](#53-publier)).

#### 4.6.2 Actions à faire dans GTM pour la nouvelle URL

**a) Variable du domaine de vente — obligatoire**

GTM → **Variables** → `Qweekle - CONST - [A CONFIGURER] URL du site de VEL` → remplacer le domaine de démo par le domaine live (par exemple `demo-nom-du-client.qweekle.shop` → `client.qweekle.shop`).

Cette variable alimente le Conversion Linker Google Ads. Si elle reste sur le domaine de démo, le GCLID n'est plus transmis lors du passage vers le site de paiement et **les conversions Google Ads ne sont plus attribuées** (voir [section 4.2](#42-google-ads--conversion-linker-cross-domaine)).

> Saisir le domaine **sans** `https://` ni barre oblique finale : `client.qweekle.shop`.

**b) Vérifier les autres variables de domaine**

Toujours dans **Variables**, contrôler les deux autres constantes du module Google Ads :

| Variable | À vérifier |
|---|---|
| `Qweekle - CONST - URL du site de paiement` | Déjà renseignée (`payments.qweekle.app`) — inchangée entre démo et live, aucune action |
| `Qweekle - CONST - [A CONFIGURER] URL site vitrine` | À renseigner si le client possède un site vitrine qui redirige vers le tunnel Qweekle |

**c) Mettre à jour les plateformes de destination**

Le changement de domaine se répercute en dehors de GTM :

- **GA4** : Admin → Flux de données → mettre à jour l'URL du flux web. Vérifier aussi la liste des **domaines référents exclus** (Admin → Flux de données → Paramètres de balise → Répertorier les référents indésirables) pour y remplacer le domaine de démo par le domaine live et le domaine de paiement.
- **Meta** : Business Manager → vérifier le domaine dans les paramètres du Pixel, et valider le nouveau domaine si vous utilisez Aggregated Event Measurement.
- **Google Ads** : vérifier que les URL finales des annonces pointent vers le domaine live.

**d) Retester avant publication**

Rejouer un parcours complet sur le **domaine live** en mode Aperçu (voir [section 5.1](#51-tester-avec-le-mode-aperçu-gtm)) : le mode Aperçu doit se connecter au nouveau domaine, et les tags de conversion doivent se déclencher sur un `purchase` réel.

> **Nettoyage des données de test** : les événements générés pendant la phase de démo restent dans GA4. Ils ne peuvent pas être supprimés rétroactivement, mais vous pouvez marquer la date de bascule (GA4 → Admin → **Annotations**) pour interpréter correctement l'historique, ou exclure la période concernée de vos rapports.

---

## 5. Validation et publication

### 5.1 Tester avec le mode Aperçu GTM

1. GTM → cliquer sur **Aperçu**
2. Saisir l'URL du site Qweekle → **Connecter**
3. Naviguer sur le site et vérifier dans le panneau Tag Assistant :

| Ce qu'il faut vérifier | Résultat attendu |
|---|---|
| Balise de votre CMP | Se déclenche en premier, sur « Initialisation de la collecte du consentement » |
| Tags GA4/Meta/Ads **avant** acceptation cookies | Ne se déclenchent **pas** |
| Tags GA4/Meta/Ads **après** acceptation cookies | Se déclenchent sur les bons événements |
| **Première visite** : cookies effacés, URL d'arrivée avec `?gclid=test&utm_source=test` | À l'acceptation des cookies, `[GA4] Configuration`, `[Google Ads] Configuration`, `[Google Ads] Conversion Linker` et `[Meta] Pixel Base + PageView` se déclenchent sur l'événement de consentement (déclencheurs `Qweekle - CE - Arrivee …`) |
| Visiteur ayant déjà consenti : rechargement puis navigation interne | Les 4 balises d'arrivée se déclenchent une seule fois, sur `gtm.js`, puis plus sur les événements suivants |
| `Qweekle - DLV - ecommerce.value` sur purchase | Valeur en euros (pas en centimes) |
| `Qweekle - DLV - ecommerce.items` | Tableau non vide avec `item_id`, `price`, `quantity` |

> Si un tag se déclenche avant l'acceptation des cookies → voir [section 8](#8-dépannage).

### 5.2 Vérifier dans chaque plateforme

**GA4 — Rapport temps réel**

GA4 → Rapports → **Temps réel** : les événements ecommerce apparaissent au fil de la navigation.

Pour un diagnostic plus précis, activer le **mode Debug** :
1. Installer l'extension Chrome **Google Analytics Debugger**
2. L'activer avant de naviguer sur le site en mode Aperçu GTM
3. GA4 → Admin → **DebugView** : chaque événement apparaît en temps réel avec tous ses paramètres et valeurs

---

**Meta — Activité de test**

Meta → Business Manager → Gestionnaire d'événements → Pixel → **Activité de test** : saisir l'URL du site et naviguer pour voir les événements reçus en temps réel.

Pour valider côté navigateur, installer l'extension Chrome **Meta Pixel Helper** : elle indique quels événements sont envoyés sur chaque page et signale les erreurs éventuelles.

---

**Google Ads — Conversions**

Google Ads → Outils → Conversions : la conversion Purchase passe en statut **"Enregistrement de conversions"** après la première conversion validée (peut prendre jusqu'à 24h).

### 5.3 Publier

1. GTM → cliquer sur **Envoyer**
2. Choisir **Publier et créer une version**
3. Nommer la version (ex : `Qweekle Tracking - Setup initial`)
4. Cliquer sur **Publier**

---

## 6. Référence complète des éléments

### 6.1 Module Base

#### Variables DataLayer — `Qweekle - DLV -`

Ces variables lisent directement les clés poussées par Qweekle dans le `dataLayer`. Elles sont utilisées par tous les autres modules.

| Variable | Clé dataLayer lue | Valeur par défaut | Description |
|---|---|---|---|
| `Qweekle - DLV - ecommerce` | `ecommerce` | — | Objet ecommerce complet du dernier événement |
| `Qweekle - DLV - ecommerce.items` | `ecommerce.items` | — | Tableau des produits de l'événement |
| `Qweekle - DLV - ecommerce.value` | `ecommerce.value` | — | Valeur de commande (en euros) — jamais minorée par un bon cadeau ou un acompte |
| `Qweekle - DLV - ecommerce.currency` | `ecommerce.currency` | `EUR` | Code devise ISO |
| `Qweekle - DLV - ecommerce.affiliation` | `ecommerce.affiliation` | — | Slug de l'établissement (utile si un conteneur est mutualisé entre plusieurs établissements) |
| `Qweekle - DLV - ecommerce.transaction_id` | `ecommerce.transaction_id` | — | Identifiant unique de commande |
| `Qweekle - DLV - ecommerce.coupon` | `ecommerce.coupon` | — | Code de réduction éventuel appliqué |
| `Qweekle - DLV - ecommerce.payment_type` | `ecommerce.payment_type` | — | Mode de paiement (ex. `external`) |
| `Qweekle - DLV - ecommerce.shipping_tier` | `ecommerce.shipping_tier` | — | Mode retenu à l'étape réservation |
| `Qweekle - DLV - user.user_id` | `user.user_id` | — | ID de l'utilisateur connecté |
| `Qweekle - DLV - user.email_sha256` | `user.email_sha256` | — | Hash SHA-256 de l'email de l'utilisateur |
| `Qweekle - DLV - amount_paid` | `amount_paid` | — | Montant encaissé en ligne (acompte), sur `purchase` |
| `Qweekle - DLV - amount_due` | `amount_due` | — | Solde réglé sur place, sur `purchase` |
| `Qweekle - DLV - gift_card_amount` | `gift_card_amount` | — | Part réglée en bon cadeau, sur `purchase` |

#### Triggers — `Qweekle - CE -`

| Trigger | Type | Événement écouté |
|---|---|---|
| `Qweekle - CE - view_item_list` | Custom Event | `view_item_list` |
| `Qweekle - CE - view_item` | Custom Event | `view_item` |
| `Qweekle - CE - add_to_cart` | Custom Event | `add_to_cart` |
| `Qweekle - CE - remove_from_cart` | Custom Event | `remove_from_cart` |
| `Qweekle - CE - view_cart` | Custom Event | `view_cart` |
| `Qweekle - CE - begin_checkout` | Custom Event | `begin_checkout` |
| `Qweekle - CE - add_shipping_info` | Custom Event | `add_shipping_info` |
| `Qweekle - CE - add_payment_info` | Custom Event | `add_payment_info` |
| `Qweekle - CE - purchase` | Custom Event | `purchase` |
| `Qweekle - CE - login` | Custom Event | `login` |
| `Qweekle - CE - sign_up` | Custom Event | `sign_up` |
| `Qweekle - CE - Tous les evenements ecommerce` | Custom Event (regex) | Tous les événements ecommerce en une seule règle |
| `Qweekle - CE - Arrivee analytics accorde` | Custom Event (regex) + condition | Chargement, mise à jour du consentement ou `page_view`, si `analytics_storage` est accordé (voir [section 4.1](#relance-des-balises-après-consentement)) |
| `Qweekle - CE - Arrivee publicite accordee` | Custom Event (regex) + condition | Mêmes événements, si `ad_storage` et `ad_user_data` sont accordés |

Le trigger regex écoute le pattern :
```
^(view_item_list|view_item|add_to_cart|remove_from_cart|view_cart|begin_checkout|add_shipping_info|add_payment_info|purchase)$
```

Les deux triggers d'arrivée écoutent le pattern :
```
^(gtm\.js|cookie_consent_update|axeptio_update|didomi-consent|page_view)$
```

#### Variables de consentement — `Qweekle - CONSENT -`

Basées sur le modèle de la galerie **GTM Consent State** (Ayudante), elles renvoient `true` si le type de consentement est accordé au moment de l'événement.

| Variable | Type de consentement lu |
|---|---|
| `Qweekle - CONSENT - analytics_storage` | `analytics_storage` |
| `Qweekle - CONSENT - ad_storage` | `ad_storage` |
| `Qweekle - CONSENT - ad_user_data` | `ad_user_data` |

#### Tags

Aucun. Le module Base ne contient que des variables et des déclencheurs : le consentement est géré par le modèle GTM de votre CMP (voir [section 3.1.1](#311-consent-mode--pourquoi-et-comment-configurer)).

---

### 6.2 Module GA4

#### Paramètres de consentement

Tous les tags de ce module requièrent `analytics_storage`. Ce paramètre est déjà configuré dans les fichiers importés — aucune action manuelle n'est nécessaire.

#### Variable Constante

| Variable | Valeur par défaut | Description |
|---|---|---|
| `Qweekle - CONST - [A CONFIGURER] GA4 Measurement ID` | `G-XXXXXXXXXX` | Identifiant de la propriété GA4 du client |

#### Variable Custom JavaScript

**`Qweekle - CJS - GA4 User ID`**
Retourne le `user.user_id` depuis le dataLayer, ou `undefined` si l'utilisateur n'est pas connecté. Utilisé dans les user properties GA4.

#### Tags

**`[GA4] Configuration`**
- Type : Balise Google (`googtag`)
- Déclenchement : `Qweekle - CE - Arrivee analytics accorde`, une fois par page
- Consentement requis : `analytics_storage`
- Paramètre `tagId` : `{{Qweekle - CONST - [A CONFIGURER] GA4 Measurement ID}}`
- Envoie le `user_id` si l'utilisateur est connecté

**`[GA4] Evenements Ecommerce`**
- Type : Événement GA4 (`gaawe`)
- Déclenchement : `Qweekle - CE - Tous les evenements ecommerce`
- Consentement requis : `analytics_storage`
- L'objet `ecommerce` est lu depuis le dataLayer : `affiliation`, `value`, `items`, `transaction_id`, `coupon`, `payment_type`, `shipping_tier` sont transmis automatiquement à GA4
- Envoie 3 paramètres custom sur `purchase` : `amount_paid`, `amount_due`, `gift_card_amount` (absents des autres événements — voir [DATALAYER-REFERENCE.md](DATALAYER-REFERENCE.md), section 6)

> 💡 Pour exploiter `amount_paid`, `amount_due` et `gift_card_amount` dans les rapports, créez les définitions personnalisées correspondantes dans GA4 (Admin → Définitions personnalisées → Métriques personnalisées, portée Événement, unité Devise).

**`[GA4] login`** — Déclenchement : `Qweekle - CE - login` · Envoie le `user_id` en user property

**`[GA4] sign_up`** — Déclenchement : `Qweekle - CE - sign_up` · Envoie le `user_id` en user property

---

### 6.3 Module Meta

> Ce module inclut le template Facebook Pixel de Simo Ahava (référence communautaire officielle). Il sera disponible dans GTM → Modèles après l'import.

#### Paramètres de consentement

Tous les tags de ce module requièrent `ad_storage` et `ad_user_data`. Ces paramètres sont déjà configurés dans les fichiers importés — aucune action manuelle n'est nécessaire.

#### Advanced Matching

L'Advanced Matching est activé sur tous les tags Meta. L'email hashé (`user.email_sha256`) et le user ID (`user.user_id`) sont envoyés automatiquement sur chaque événement quand ils sont présents dans le dataLayer.

#### Variable Constante

| Variable | Valeur par défaut | Description |
|---|---|---|
| `Qweekle - CONST - [A CONFIGURER] Meta Pixel ID` | `000000000000000` | Identifiant du Pixel Meta du client |

#### Variables Custom JavaScript

**`Qweekle - CJS - Meta Event Props`** — Construit l'objet propriétés pour ViewContent, AddToCart, InitiateCheckout (`content_ids`, `contents`, `content_type`, `value`, `currency`). Ajoute `content_category` depuis `item_category2` (catégorie catalogue, stable) du premier produit si disponible.

**`Qweekle - CJS - Meta Purchase Props`** — Identique, avec `order_id` en plus pour la déduplication API Conversions et `content_category` depuis `item_category2` du premier produit.

#### Tags

Tous les tags Meta partagent : `disablePushState: true`, `advancedMatching: true`, consentement `ad_storage` + `ad_user_data`.

| Tag | Déclencheur | Événement Meta |
|---|---|---|
| `[Meta] Pixel Base + PageView` | `Qweekle - CE - Arrivee publicite accordee` (une fois par page) | `PageView` |
| `[Meta] ViewContent` | `Qweekle - CE - view_item` | `ViewContent` |
| `[Meta] AddToCart` | `Qweekle - CE - add_to_cart` | `AddToCart` |
| `[Meta] InitiateCheckout` | `Qweekle - CE - begin_checkout` | `InitiateCheckout` |
| `[Meta] Purchase` | `Qweekle - CE - purchase` | `Purchase` |

---

### 6.4 Module Google Ads

#### Paramètres de consentement

| Tag | Consentement requis |
|---|---|
| `[Google Ads] Configuration` | `ad_storage`, `ad_user_data` |
| `[Google Ads] Conversion Linker` | `ad_storage` |
| `[Google Ads] Conversion - Purchase` | `ad_storage`, `ad_user_data` |
| `[Google Ads] Remarketing` | `ad_storage`, `ad_user_data` |

Ces paramètres sont déjà configurés dans les fichiers importés — aucune action manuelle n'est nécessaire.

#### Cross-domain

Le cross-domain est activé — les domaines sont lus depuis les trois variables CONST (voir [section 4.2](#42-google-ads--conversion-linker-cross-domaine)).

#### Variables Constantes

| Variable | Valeur par défaut | Description |
|---|---|---|
| `Qweekle - CONST - [A CONFIGURER] Google Ads Conversion ID` | `AW-XXXXXXXXXX` | Identifiant du compte Google Ads du client |
| `Qweekle - CONST - [A CONFIGURER] Google Ads Conversion Label` | `XXXXXXXXXXXXXXXXXXX` | Libellé de la conversion Purchase |
| `Qweekle - CONST - [A CONFIGURER] URL du site de VEL` | `client.qweekle.shop` | Domaine du site Qweekle du client |
| `Qweekle - CONST - URL du site de paiement` | `payments.qweekle.app` | Domaine du tunnel de paiement |
| `Qweekle - CONST - [A CONFIGURER] URL site vitrine` | `monsite.fr` | Domaine propre du client s'il en possède un |

#### Variable Custom JavaScript

**`Qweekle - CJS - User Data (Enhanced Conversions)`** — Construit l'objet `{ sha256_email_address, external_id }` pour les Enhanced Conversions. Retourne `undefined` si ni l'email ni le user_id ne sont disponibles.

#### Tags

| Tag | Déclencheur | Consentement |
|---|---|---|
| `[Google Ads] Configuration` | `Qweekle - CE - Arrivee publicite accordee` (une fois par page) | `ad_storage`, `ad_user_data` |
| `[Google Ads] Conversion Linker` | `Qweekle - CE - Arrivee publicite accordee` (une fois par page) | `ad_storage` |
| `[Google Ads] Conversion - Purchase` | `Qweekle - CE - purchase` | `ad_storage`, `ad_user_data` |
| `[Google Ads] Remarketing` | `Qweekle - CE - view_item` | `ad_storage`, `ad_user_data` |

La conversion Purchase envoie valeur, devise, order_id et les données Enhanced Conversions quand disponibles (voir [section 4.4](#44-enhanced-conversions--google-ads)).

> La valeur envoyée (`ecommerce.value`) est la **valeur de commande complète** : elle n'est jamais minorée par un bon cadeau ou un acompte (voir [DATALAYER-REFERENCE.md](DATALAYER-REFERENCE.md), section 6). Le ROAS Google Ads reflète donc le chiffre d'affaires réel de la commande.

---

## 7. Glossaire

| Terme | Définition |
|---|---|
| **dataLayer** | Tableau de données invisible sur votre site, alimenté automatiquement par Qweekle. GTM y lit les événements (visite, achat…) pour les envoyer aux plateformes. |
| **GTM (Google Tag Manager)** | Outil de gestion des balises de suivi. Permet d'installer et configurer GA4, Meta, Google Ads sans toucher au code du site. |
| **Tag / Balise** | Morceau de code qui envoie des données à une plateforme. Chaque tag se déclenche sur un événement précis. |
| **Trigger / Déclencheur** | Condition qui active un tag. Exemple : le trigger `purchase` active les tags de conversion quand une commande est passée. |
| **DLV (DataLayer Variable)** | Variable GTM qui lit une valeur dans le dataLayer. Exemple : `ecommerce.value` lit le montant de la commande. |
| **CONST (Constante)** | Variable GTM dont la valeur est fixe, renseignée une fois par client. Exemple : l'ID de la propriété GA4. |
| **CJS (Custom JavaScript)** | Variable GTM contenant une fonction JavaScript qui transforme ou combine des données avant de les envoyer. |
| **Consent Mode** | Mécanisme Google qui bloque les tags de mesure tant que l'utilisateur n'a pas accepté les cookies. Obligatoire en Europe (RGPD). |
| **CMP (Consent Management Platform)** | La bannière cookies du site : Axeptio, Didomi, Cookiebot, CookieYes ou autre. Elle recueille le consentement de l'utilisateur. |
| **RGPD** | Règlement Général sur la Protection des Données. Réglementation européenne qui impose de recueillir le consentement avant de collecter des données sur les visiteurs. |
| **Fusion** | Méthode d'import GTM qui ajoute les éléments importés à ceux existants, sans rien supprimer. À toujours préférer à "Écraser". |
| **GCLID** | Identifiant de clic ajouté par Google Ads à l'URL quand un visiteur clique sur une publicité. Permet d'attribuer une conversion à la bonne annonce. |
| **Cross-domain** | Mécanisme qui transmet le GCLID entre deux domaines différents (ex : `monsite.fr` → `client.qweekle.shop`). Sans lui, les conversions multi-domaines ne sont pas attribuées. |
| **Enhanced Conversions** | Fonctionnalité Google Ads et GA4 qui améliore la précision des conversions en envoyant des données utilisateur hachées (email, user ID). |
| **Advanced Matching** | Fonctionnalité Meta équivalente aux Enhanced Conversions. Améliore la précision des audiences et des conversions Meta. |
| **SHA-256** | Algorithme qui transforme une donnée sensible (ex : email) en une chaîne de caractères illisible. Permet d'envoyer des données utilisateur sans exposer les informations personnelles. |
| **ecommerce** | Objet standard qui décrit un événement commercial : liste de produits, prix, devise, identifiant de transaction. |
| **Affiliation** | Slug technique de l'établissement (ex : `RE-VOL`), présent sur tous les événements. Il identifie l'établissement à l'origine de l'événement — indispensable si vous choisissez de mutualiser un même conteneur GTM ou une même propriété GA4 entre plusieurs établissements (configuration optionnelle). |
| **Tag (catégorie en ligne)** | Le champ `item_category` d'un produit : l'univers de merchandising d'où le produit a été ajouté au panier (carrousel, header). Figé par ligne de panier jusqu'au purchase ; vaut `(direct)` si ajout sans contexte de liste. Les champs `item_category2/3/4` décrivent en revanche le produit dans le catalogue (stables). |
| **VEL (Vente En Ligne)** | Le site de boutique Qweekle du client (ex : `client.qweekle.shop`). |
| **SPA (Single Page Application)** | Architecture web où la page ne se recharge pas entièrement lors de la navigation. Le paramètre `disablePushState` sur les tags Meta évite les doublons dans ce contexte. |

---

## 8. Dépannage

**Les tags se déclenchent avant le consentement**
Vérifier que votre CMP est installée avec son modèle GTM, sur **Initialisation du consentement - Toutes les pages**, et que son **consentement par défaut est sur « refusé »** (voir [section 3.1.1](#311-consent-mode--pourquoi-et-comment-configurer)). Un défaut sur « accordé » laisse partir les balises avant le choix du visiteur, selon la vitesse de chargement de la bannière.

**Les nouveaux visiteurs de vos campagnes ne sont pas attribués** (sessions en direct ou en recherche naturelle dans GA4, conversions Google Ads non rattachées aux clics)
Tester une première visite en mode Aperçu, cookies effacés, avec une URL d'arrivée portant `?gclid=test&utm_source=test`. À l'acceptation des cookies, les balises d'arrivée doivent se déclencher sur l'événement de consentement (déclencheurs `Qweekle - CE - Arrivee …`). Si elles ne partent qu'à la page suivante (sur `page_view`), votre CMP pousse un événement que les déclencheurs ne connaissent pas : repérer son nom dans l'onglet **Data Layer** du mode Aperçu, puis l'ajouter à leur expression régulière (voir [section 4.1](#relance-des-balises-après-consentement)). Si elles ne partent jamais, vérifier dans l'onglet **Variables** que `Qweekle - CONSENT - …` vaut bien `true` après l'acceptation.

**Une variable CJS retourne `undefined` ou `{}`**
Ouvrir la console navigateur, taper `dataLayer` et vérifier que `user.user_id` et `user.email_sha256` sont bien présents. Si les champs sont vides, les variables retournent `undefined` intentionnellement — aucune donnée n'est envoyée vers les plateformes.

**Dans GA4, presque tout le chiffre d'affaires vient de `payments.qweekle.app / referral`**

Le domaine de paiement n'est pas exclu des référents. Au retour du paiement, GA4 ouvre une nouvelle session attribuée à ce domaine et y range le `purchase`, ce qui efface la source d'acquisition réelle. Ajouter `payments.qweekle.app` aux **référents indésirables** (voir [section 3.2](#32-module-ga4--mise-en-route-minimale)).

> L'exclusion n'est pas rétroactive : les sessions déjà enregistrées gardent leur attribution erronée. Seules les données postérieures au changement sont correctes.

**Aucun événement pendant le paiement**
C'est normal : le site de paiement ne charge pas GTM. L'événement `purchase` est émis au retour sur la page de confirmation du site de vente. Si le `purchase` n'apparaît pas après un paiement réussi, vérifier que le retour aboutit bien sur la page de confirmation (`/checkout/confirmation`).

**L'événement purchase ne remonte pas dans Google Ads**
Vérifier que `Qweekle - DLV - ecommerce.value` est non nul (Google Ads ignore les conversions à 0). Vérifier que `Qweekle - DLV - ecommerce.transaction_id` est unique à chaque commande pour éviter la déduplication.

**Les données Meta sont vides ou incorrectes**
Dans le mode Aperçu, inspecter les valeurs de `Qweekle - CJS - Meta Event Props` et `Qweekle - CJS - Meta Purchase Props`. Si `ecommerce.items` n'est pas un tableau valide, les CJS retournent `{}` et aucune propriété n'est envoyée.

**Le Pixel Meta se déclenche deux fois**
Vérifier que `disablePushState` est bien à `true` sur tous les tags Meta. Vérifier qu'aucun autre tag Pixel Meta n'existe déjà dans le container.

**L'import génère des doublons de variables ou triggers**
GTM peut créer des doublons si des éléments portent le même nom que des éléments existants. Après l'import, vérifier dans GTM → Variables et GTM → Déclencheurs que chaque nom n'apparaît qu'une seule fois. Supprimer les doublons en conservant la version importée.

**Les conversions Google Ads ne sont pas attribuées malgré des clics sur les annonces**
Vérifier que `URL du site de VEL` contient le bon domaine. Si vous avez votre propre site, vérifier que `URL site vitrine` est également renseigné (voir [section 4.2](#42-google-ads--conversion-linker-cross-domaine)).
