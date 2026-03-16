# Documentation — Modules GTM Qweekle

> **Version** : 1.0 — 16/03/2026
> **Audience** : clients Qweekle et agences marketing
> Pour la référence technique complète du dataLayer, voir [DATALAYER-REFERENCE.md](DATALAYER-REFERENCE.md)

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

### Les 4 modules

```
┌──────────────────────────────────────────────────────────────┐
│                    qweekle-1-base.json                       │
│         Variables DLV · Triggers · Consent Mode             │
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

**Le module Base est obligatoire.** Il contient les variables de lecture du dataLayer, les déclencheurs partagés entre tous les modules, et le Consent Mode (gestion du consentement RGPD).

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

> 💡 **Conseil** : créer un espace de travail dédié avant l'import (GTM → Espaces de travail → `+`) pour pouvoir isoler les changements et les annuler si nécessaire.

---

## 3. Mise en route minimale

Après import, les seules actions requises sont de **renseigner vos identifiants de plateformes** et de **configurer votre bannière cookies**. Tout le reste est préconfiguré.

### 3.1 Module Base — obligatoire pour tous

Aucun identifiant à renseigner. La seule action requise est de connecter votre bannière cookies au Consent Mode.

#### 3.1.1 Consent Mode — pourquoi et comment configurer

**Pourquoi c'est obligatoire** : le RGPD interdit de collecter des données sur les visiteurs européens sans leur accord. Le Consent Mode garantit qu'aucun tag (GA4, Meta, Google Ads) ne se déclenche avant que l'utilisateur ait accepté les cookies. Sans cette configuration, votre client s'expose à des sanctions légales.

**Procédure (5 minutes) :**

1. GTM → **Tags** → ouvrir `[Qweekle] Consent Mode - CMP Update [A CONFIGURER]`
2. Localiser le bloc correspondant à votre bannière cookies (Axeptio, Didomi ou Cookiebot)
3. Supprimer les `/*` et `*/` qui l'entourent — uniquement ce bloc
4. Sauvegarder

Pour les détails de personnalisation par CMP (clés Axeptio, IDs Didomi), voir [section 4.1](#41-consent-mode--intégration-cmp-détaillée).

---

### 3.2 Module GA4 — mise en route minimale

**Information à récupérer :**

| Information | Où la trouver |
|---|---|
| GA4 Measurement ID | GA4 → Admin → Flux de données → flux web → format `G-XXXXXXXXXX` |

**Action après l'import :**

GTM → **Variables** → ouvrir `Qweekle - CONST - [A CONFIGURER] GA4 Measurement ID` → remplacer `G-XXXXXXXXXX` par l'ID du client.

> Les paramètres de consentement sont déjà configurés sur tous les tags GA4.

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

Le module est opérationnel. Pour configurer le cross-domaine (indispensable si le client a son propre nom de domaine), voir [section 4.2](#42-google-ads--conversion-linker-cross-domaine).

---

### ✅ Checklist de setup

Avant de passer à la validation, vérifier que chaque étape est complète.

**Module Base — obligatoire**
- [ ] Module Base importé en mode **Fusion**
- [ ] Bannière cookies (CMP) décommentée dans le tag `[Qweekle] Consent Mode - CMP Update`

**Module GA4** *(si utilisé)*
- [ ] Module GA4 importé en mode **Fusion**
- [ ] `Qweekle - CONST - [A CONFIGURER] GA4 Measurement ID` renseigné

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
- [ ] Événement `purchase` vérifié dans chaque plateforme ✓
- [ ] Version publiée dans GTM ✓

---

## 4. Configurations avancées

### 4.1 Consent Mode — intégration CMP détaillée

Le tag `[Qweekle] Consent Mode - CMP Update` contient les blocs de code pour trois CMP, tous commentés. Après avoir décommenté le bon bloc (voir [section 3.1.1](#311-consent-mode--pourquoi-et-comment-configurer)), il peut être nécessaire d'adapter les identifiants propres au projet du client.

---

**Axeptio** — adapter les clés `choices.google_analytics`, `choices.meta_pixel`, `choices.google_ads` aux noms des vendors configurés dans le projet Axeptio du client :

```javascript
void 0 === window._axcb && (window._axcb = []);
window._axcb.push(function(sdk) {
  sdk.on('cookies:complete', function(choices) {
    function gtag(){dataLayer.push(arguments);}
    gtag('consent', 'update', {
      'analytics_storage':  choices.google_analytics ? 'granted' : 'denied',
      'ad_storage':         (choices.meta_pixel || choices.google_ads) ? 'granted' : 'denied',
      'ad_user_data':       (choices.meta_pixel || choices.google_ads) ? 'granted' : 'denied',
      'ad_personalization': (choices.meta_pixel || choices.google_ads) ? 'granted' : 'denied'
    });
  });
});
```

---

**Didomi** — adapter les IDs de purpose `analytics` et `advertising` aux IDs configurés dans le dashboard Didomi du client :

```javascript
window.didomiOnReady = window.didomiOnReady || [];
window.didomiOnReady.push(function(Didomi) {
  function gtag(){dataLayer.push(arguments);}
  gtag('consent', 'update', {
    'analytics_storage':  Didomi.getUserConsentStatusForPurpose('analytics') ? 'granted' : 'denied',
    'ad_storage':         Didomi.getUserConsentStatusForPurpose('advertising') ? 'granted' : 'denied',
    'ad_user_data':       Didomi.getUserConsentStatusForPurpose('advertising') ? 'granted' : 'denied',
    'ad_personalization': Didomi.getUserConsentStatusForPurpose('advertising') ? 'granted' : 'denied'
  });
});
```

---

**Cookiebot** — aucun identifiant à adapter :

```javascript
window.addEventListener('CookiebotOnAccept', function() {
  function gtag(){dataLayer.push(arguments);}
  gtag('consent', 'update', {
    'analytics_storage':  Cookiebot.consent.statistics ? 'granted' : 'denied',
    'ad_storage':         Cookiebot.consent.marketing ? 'granted' : 'denied',
    'ad_user_data':       Cookiebot.consent.marketing ? 'granted' : 'denied',
    'ad_personalization': Cookiebot.consent.marketing ? 'granted' : 'denied'
  });
}, false);
```

---

**Autre CMP** : implémenter la même logique — écouter l'événement de consentement de la CMP, puis appeler `gtag('consent', 'update', { ... })` avec `'granted'` ou `'denied'` selon les choix de l'utilisateur.

---

### 4.2 Google Ads — Conversion Linker cross-domaine

Le Conversion Linker est préconfiguré avec `enableCrossDomain: true` et trois variables de domaine. Renseigner celles qui s'appliquent à votre configuration :

| Variable | Valeur par défaut | Quand la renseigner |
|---|---|---|
| `Qweekle - CONST - [A CONFIGURER] URL du site de VEL` | `client.qweekle.shop` | Toujours — remplacer par le vrai domaine du site Qweekle du client |
| `Qweekle - CONST - URL du site de paiement` | `paiement.qweekle.shop` | Déjà renseignée par défaut, à ajuster si besoin |
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

Si le client utilise l'API Conversions Meta côté serveur en parallèle du Pixel navigateur, la déduplication est déjà prête. Le tag `[Meta] Purchase` envoie un `order_id` (valeur de `Qweekle - DLV - ecommerce.transaction_id`) qui sert d'`event_id` pour la déduplication entre les hits navigateur et serveur. Aucune configuration supplémentaire dans GTM.

---

## 5. Validation et publication

### 5.1 Tester avec le mode Aperçu GTM

1. GTM → cliquer sur **Aperçu**
2. Saisir l'URL du site Qweekle → **Connecter**
3. Naviguer sur le site et vérifier dans le panneau Tag Assistant :

| Ce qu'il faut vérifier | Résultat attendu |
|---|---|
| Tags Consent Mode | Se déclenchent en premier sur chaque page |
| Tags GA4/Meta/Ads **avant** acceptation cookies | Ne se déclenchent **pas** |
| Tags GA4/Meta/Ads **après** acceptation cookies | Se déclenchent sur les bons événements |
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
| `Qweekle - DLV - ecommerce.value` | `ecommerce.value` | — | Valeur monétaire de l'événement (en euros) |
| `Qweekle - DLV - ecommerce.currency` | `ecommerce.currency` | `EUR` | Code devise ISO |
| `Qweekle - DLV - ecommerce.transaction_id` | `ecommerce.transaction_id` | — | Identifiant unique de commande |
| `Qweekle - DLV - ecommerce.coupon` | `ecommerce.coupon` | — | Code promo éventuel appliqué |
| `Qweekle - DLV - user.user_id` | `user.user_id` | — | ID de l'utilisateur connecté |
| `Qweekle - DLV - user.email_sha256` | `user.email_sha256` | — | Hash SHA-256 de l'email de l'utilisateur |
| `Qweekle - DLV - payment_type` | `payment_type` | — | Mode de paiement (`card`, `gift_card`, `gift_card+card`) |
| `Qweekle - DLV - checkout_type` | `checkout_type` | — | Mode de tunnel (`guest`, `login`, `signup`) |
| `Qweekle - DLV - search_term` | `search_term` | — | Terme saisi dans la recherche |
| `Qweekle - DLV - navigation_context` | `navigation_context` | — | Contexte de navigation (liste, recherche, page produit…) |

#### Triggers — `Qweekle - CE -`

| Trigger | Type | Événement écouté |
|---|---|---|
| `All Pages` | Page View | Toutes les pages |
| `Qweekle - CE - view_item_list` | Custom Event | `view_item_list` |
| `Qweekle - CE - select_item` | Custom Event | `select_item` |
| `Qweekle - CE - view_item` | Custom Event | `view_item` |
| `Qweekle - CE - add_to_cart` | Custom Event | `add_to_cart` |
| `Qweekle - CE - remove_from_cart` | Custom Event | `remove_from_cart` |
| `Qweekle - CE - view_cart` | Custom Event | `view_cart` |
| `Qweekle - CE - begin_checkout` | Custom Event | `begin_checkout` |
| `Qweekle - CE - add_payment_info` | Custom Event | `add_payment_info` |
| `Qweekle - CE - purchase` | Custom Event | `purchase` |
| `Qweekle - CE - search` | Custom Event | `search` |
| `Qweekle - CE - login` | Custom Event | `login` |
| `Qweekle - CE - sign_up` | Custom Event | `sign_up` |
| `Qweekle - CE - Tous les evenements ecommerce` | Custom Event (regex) | Tous les événements ecommerce en une seule règle |

Le trigger regex écoute le pattern :
```
^(view_item_list|select_item|view_item|add_to_cart|remove_from_cart|view_cart|begin_checkout|add_payment_info|purchase)$
```

#### Tags

**`[Qweekle] Consent Mode - Default`**
- Type : HTML personnalisé
- Déclenchement : `All Pages`, `ONCE_PER_LOAD`, sans condition de consentement
- Rôle : initialise le Consent Mode Google en plaçant tous les états en `denied` avant toute interaction de l'utilisateur. Active également `ads_data_redaction` et `url_passthrough` pour conserver une mesure partielle même sans consentement.

**`[Qweekle] Consent Mode - CMP Update [A CONFIGURER]`**
- Type : HTML personnalisé
- Déclenchement : `All Pages`, `ONCE_PER_LOAD`, sans condition de consentement
- Rôle : écoute la décision de l'utilisateur via la CMP et met à jour les états de consentement. Contient les blocs pour Axeptio, Didomi et Cookiebot à décommenter (voir [section 3.1.1](#311-consent-mode--pourquoi-et-comment-configurer)).

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
- Déclenchement : `All Pages`
- Consentement requis : `analytics_storage`
- Paramètre `tagId` : `{{Qweekle - CONST - [A CONFIGURER] GA4 Measurement ID}}`
- Envoie le `user_id` si l'utilisateur est connecté

**`[GA4] Evenements Ecommerce`**
- Type : Événement GA4 (`gaawe`)
- Déclenchement : `Qweekle - CE - Tous les evenements ecommerce`
- Consentement requis : `analytics_storage`
- Envoie 3 paramètres custom : `navigation_context`, `checkout_type`, `payment_type`

**`[GA4] search`** — Déclenchement : `Qweekle - CE - search` · Envoie `search_term`

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

**`Qweekle - CJS - Meta Event Props`** — Construit l'objet propriétés pour ViewContent, AddToCart, InitiateCheckout (`content_ids`, `contents`, `content_type`, `value`, `currency`). Ajoute `content_category` depuis `item_category` du premier produit si disponible.

**`Qweekle - CJS - Meta Purchase Props`** — Identique, avec `order_id` en plus pour la déduplication API Conversions et `content_category` depuis `item_category` du premier produit.

#### Tags

Tous les tags Meta partagent : `disablePushState: true`, `advancedMatching: true`, consentement `ad_storage` + `ad_user_data`.

| Tag | Déclencheur | Événement Meta |
|---|---|---|
| `[Meta] Pixel Base + PageView` | `All Pages` | `PageView` |
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
| `Qweekle - CONST - URL du site de paiement` | `paiement.qweekle.shop` | Domaine du tunnel de paiement |
| `Qweekle - CONST - [A CONFIGURER] URL site vitrine` | `monsite.fr` | Domaine propre du client s'il en possède un |

#### Variable Custom JavaScript

**`Qweekle - CJS - User Data (Enhanced Conversions)`** — Construit l'objet `{ sha256_email_address, external_id }` pour les Enhanced Conversions. Retourne `undefined` si ni l'email ni le user_id ne sont disponibles.

#### Tags

| Tag | Déclencheur | Consentement |
|---|---|---|
| `[Google Ads] Configuration` | `All Pages` | `ad_storage`, `ad_user_data` |
| `[Google Ads] Conversion Linker` | `All Pages` | `ad_storage` |
| `[Google Ads] Conversion - Purchase` | `Qweekle - CE - purchase` | `ad_storage`, `ad_user_data` |
| `[Google Ads] Remarketing` | `Qweekle - CE - view_item` | `ad_storage`, `ad_user_data` |

La conversion Purchase envoie valeur, devise, order_id et les données Enhanced Conversions quand disponibles (voir [section 4.4](#44-enhanced-conversions--google-ads)).

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
| **CMP (Consent Management Platform)** | La bannière cookies du site : Axeptio, Didomi, Cookiebot ou autre. Elle recueille le consentement de l'utilisateur. |
| **RGPD** | Règlement Général sur la Protection des Données. Réglementation européenne qui impose de recueillir le consentement avant de collecter des données sur les visiteurs. |
| **Fusion** | Méthode d'import GTM qui ajoute les éléments importés à ceux existants, sans rien supprimer. À toujours préférer à "Écraser". |
| **GCLID** | Identifiant de clic ajouté par Google Ads à l'URL quand un visiteur clique sur une publicité. Permet d'attribuer une conversion à la bonne annonce. |
| **Cross-domain** | Mécanisme qui transmet le GCLID entre deux domaines différents (ex : `monsite.fr` → `client.qweekle.shop`). Sans lui, les conversions multi-domaines ne sont pas attribuées. |
| **Enhanced Conversions** | Fonctionnalité Google Ads et GA4 qui améliore la précision des conversions en envoyant des données utilisateur hachées (email, user ID). |
| **Advanced Matching** | Fonctionnalité Meta équivalente aux Enhanced Conversions. Améliore la précision des audiences et des conversions Meta. |
| **SHA-256** | Algorithme qui transforme une donnée sensible (ex : email) en une chaîne de caractères illisible. Permet d'envoyer des données utilisateur sans exposer les informations personnelles. |
| **ecommerce** | Objet standard qui décrit un événement commercial : liste de produits, prix, devise, identifiant de transaction. |
| **VEL (Vente En Ligne)** | Le site de boutique Qweekle du client (ex : `client.qweekle.shop`). |
| **SPA (Single Page Application)** | Architecture web où la page ne se recharge pas entièrement lors de la navigation. Le paramètre `disablePushState` sur les tags Meta évite les doublons dans ce contexte. |

---

## 8. Dépannage

**Les tags se déclenchent avant le consentement**
Vérifier que la CMP est bien décommentée dans le tag `[Qweekle] Consent Mode - CMP Update` (voir [section 3.1.1](#311-consent-mode--pourquoi-et-comment-configurer)). Si nécessaire, augmenter la priorité du tag Consent Mode Default : ouvrir le tag → Paramètres avancés → Priorité du déclenchement → mettre `10`.

**Une variable CJS retourne `undefined` ou `{}`**
Ouvrir la console navigateur, taper `dataLayer` et vérifier que `user.user_id` et `user.email_sha256` sont bien présents. Si les champs sont vides, les variables retournent `undefined` intentionnellement — aucune donnée n'est envoyée vers les plateformes.

**L'événement purchase ne remonte pas dans Google Ads**
Vérifier que `Qweekle - DLV - ecommerce.value` est non nul (Google Ads ignore les conversions à 0). Vérifier que `Qweekle - DLV - ecommerce.transaction_id` est unique à chaque commande pour éviter la déduplication.

**Les données Meta sont vides ou incorrectes**
Dans le mode Aperçu, inspecter les valeurs de `Qweekle - CJS - Meta Event Props` et `Qweekle - CJS - Meta Purchase Props`. Si `ecommerce.items` n'est pas un tableau valide, les CJS retournent `{}` et aucune propriété n'est envoyée.

**Le Pixel Meta se déclenche deux fois**
Vérifier que `disablePushState` est bien à `true` sur tous les tags Meta. Vérifier qu'aucun autre tag Pixel Meta n'existe déjà dans le container.

**L'import génère des doublons de variables ou triggers**
GTM peut créer des doublons si des éléments portent le même nom que des éléments existants. Après l'import, vérifier dans GTM → Variables et GTM → Déclencheurs que chaque nom n'apparaît qu'une seule fois. Supprimer les doublons en conservant la version importée.

**Les conversions Google Ads ne sont pas attribuées malgré des clics sur les annonces**
Vérifier que `URL du site de VEL` contient le bon domaine. Si le client a son propre site, vérifier que `URL site vitrine` est également renseigné (voir [section 4.2](#42-google-ads--conversion-linker-cross-domaine)).
