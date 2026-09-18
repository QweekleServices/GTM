# Référence DataLayer — Qweekle

> **Audience** : agences marketing et intégrateurs techniques
> Document complémentaire à [README.md](README.md)
>
> **Version** : 1.1 — 18/09/2026
>
> Validé contre une capture Tag Assistant réelle (4 parcours, 3 commandes payées) — voir [section 11](#11-validation-terrain-18092026).

Ce document décrit l'ensemble des événements poussés par la plateforme Qweekle dans le `dataLayer`, leur structure de données et les valeurs attendues.

---

## Table des matières

1. [Structure générale](#1-structure-générale)
2. [Le champ `affiliation`](#2-le-champ-affiliation)
3. [Objet `ecommerce`](#3-objet-ecommerce)
4. [Structure d'un `item`](#4-structure-dun-item)
5. [Objet `user`](#5-objet-user)
6. [Règles monétaires : `value`, remises, bons cadeaux, acomptes](#6-règles-monétaires--value-remises-bons-cadeaux-acomptes)
7. [Événement de page : `page_view`](#7-événement-de-page--page_view)
8. [Événements ecommerce](#8-événements-ecommerce)
9. [Événements utilisateur](#9-événements-utilisateur)
10. [Notes d'implémentation](#10-notes-dimplémentation)
11. [Validation terrain (18/09/2026)](#11-validation-terrain-18092026)

---

## 1. Structure générale

Chaque push dans le dataLayer suit la structure GA4 standard :

```javascript
window.dataLayer.push({
  event: 'nom_evenement',
  ecommerce: { ... },   // présent sur les événements ecommerce
  user: { ... },        // présent quand l'utilisateur est identifié
  // champs contextuels selon l'événement
});
```

> **Important** : avant chaque événement ecommerce, Qweekle pousse `{ ecommerce: null }` pour vider l'objet ecommerce précédent et éviter les pollutions de données entre événements.

### Liste des événements

| Événement | Catégorie | Déclencheur |
|---|---|---|
| `page_view` | Navigation | Chaque navigation réelle (SPA) |
| `view_item_list` | Ecommerce | Affichage d'une liste / carrousel de produits |
| `view_item` | Ecommerce | Affichage d'une fiche produit |
| `add_to_cart` | Ecommerce | Ajout au panier (tous les produits de l'action) |
| `remove_from_cart` | Ecommerce | Retrait du panier |
| `view_cart` | Ecommerce | Affichage du panier |
| `begin_checkout` | Ecommerce | Entrée dans le tunnel de commande |
| `add_shipping_info` | Ecommerce | Validation de l'étape réservation (pas de livraison chez Qweekle — l'événement GA4 standard est réutilisé pour cette étape du tunnel) |
| `add_payment_info` | Ecommerce | Validation des informations de paiement |
| `purchase` | Ecommerce | Confirmation de commande (retour du site de paiement) |
| `login` | Utilisateur | Connexion |
| `sign_up` | Utilisateur | Création de compte |
| `sign_out` | Utilisateur | Déconnexion |

---

## 2. Le champ `affiliation`

Le champ `affiliation` identifie l'établissement à l'origine de l'événement. Il permet — **c'est optionnel** — de mutualiser un même conteneur GTM (et une même propriété GA4) entre plusieurs établissements : chaque événement reste rattaché à son site via ce champ.

| Règle | Valeur |
|---|---|
| **Contenu** | Slug technique unique et **immuable** de l'établissement |
| **Format** | Code court ASCII MAJUSCULES, séparateur `-`. Ex. `RE-VOL` |
| **Présence** | Dans `ecommerce.affiliation` sur tous les événements ecommerce, et à la racine sur `page_view` |

```javascript
// Événement ecommerce
{ event: 'view_cart', ecommerce: { affiliation: 'RE-VOL', ... } }

// page_view
{ event: 'page_view', affiliation: 'RE-VOL', ... }
```

> ⚠️ Le slug est **figé une fois pour toutes** : c'est la clé de segmentation par site dans GA4. Ce n'est jamais le nom d'affichage du site.

---

## 3. Objet `ecommerce`

### Structure complète

```javascript
ecommerce: {
  currency:       "EUR",           // toujours présent
  affiliation:    "RE-VOL",        // slug du site — toujours présent
  value:          1093,            // valeur monétaire de l'événement, en euros (float)
  transaction_id: "OXXX…",         // purchase uniquement — unique par commande
  coupon:         "PROMO10",       // code de réduction appliqué (optionnel)
  tax:            0,               // purchase — TVA si applicable
  shipping:       0,               // purchase — frais si applicables
  shipping_tier:  "Réservation",   // add_shipping_info uniquement
  payment_type:   "external",      // add_payment_info et purchase
  items: [ /* voir section 4 */ ]
}
```

### Détail des champs

| Champ | Type | Présence | Description |
|---|---|---|---|
| `currency` | string | Tous les événements | Code devise ISO 4217. Valeur fixe : `EUR` |
| `affiliation` | string | Tous les événements | Slug du site (voir [section 2](#2-le-champ-affiliation)) |
| `value` | float | Sauf `view_item_list` | Valeur monétaire de l'événement en euros (voir [section 6](#6-règles-monétaires--value-remises-bons-cadeaux-acomptes)) |
| `transaction_id` | string | `purchase` | Identifiant unique de la commande |
| `coupon` | string | Optionnel | Code de **réduction** appliqué à la commande (pas les bons cadeaux — voir section 6) |
| `tax` / `shipping` | float | `purchase` | TVA / frais, si applicables |
| `shipping_tier` | string | `add_shipping_info` | Mode retenu à l'étape réservation (ex. `Réservation`) |
| `payment_type` | string | `add_payment_info`, `purchase` | Mode de paiement (ex. `external` = redirection vers le site de paiement) |
| `item_list_id` | string | `view_item_list` | Slug de la liste affichée (kebab-case ASCII) |
| `item_list_name` | string | `view_item_list` | Libellé lisible de la liste |
| `items` | array | Tous les événements | Tableau des produits concernés (voir section 4) |

---

## 4. Structure d'un `item`

```javascript
{
  item_id:        "PXXXa13ee922d27541bab805d442dac91861",
  item_name:      "Journée Magique Illimitée",
  item_brand:     "RÊVOLUTION",          // marque / nom du site — cohérent par site
  item_category:  "Activités",           // LE TAG — contexte d'affichage (voir 4.2)
  item_category2: "Entrées & Accès",     // catégorie catalogue
  item_category3: "Billets Journée",     // sous-catégorie catalogue
  item_category4: "TICKET",              // type de produit
  price:          18,                    // prix unitaire en euros, net de réduction
  quantity:       1,
  index:          2,                     // position dans la liste (événements de liste)
  item_list_id:   "activites",           // liste d'origine (slug)
  item_list_name: "Activités"            // liste d'origine (libellé)
}
```

### 4.1 Détail des champs

| Champ | Type | Présence | Description |
|---|---|---|---|
| `item_id` | string | Toujours | Identifiant unique du produit |
| `item_name` | string | Toujours | Nom du produit |
| `item_brand` | string | Toujours | Marque (nom du site/parc), identique pour tous les produits d'un site |
| `item_category` | string | Toujours | **Le tag** : univers merchandising d'où le produit a été ajouté (voir 4.2) |
| `item_category2` | string | Toujours | Catégorie dans le catalogue produit |
| `item_category3` | string | Toujours | Sous-catégorie dans le catalogue produit |
| `item_category4` | string | Toujours | Type de produit. Valeurs : `TICKET`, `PACK`, `GIFTCARD`, `A` (activité), `S` (souvenir/service) |
| `price` | float | Toujours | Prix unitaire en euros, **net de réduction** (voir section 6) |
| `quantity` | integer | Sauf `view_item_list` | Quantité |
| `discount` | float | Optionnel | Montant remisé **par unité** (en euros, pas un %), si code de réduction |
| `coupon` | string | Optionnel | Code de réduction au niveau item |
| `index` | integer | Événements de liste | Position du produit dans la liste |
| `item_list_id` | string | Voir 4.2 | Slug de la liste d'où le produit a été découvert |
| `item_list_name` | string | Voir 4.2 | Libellé de cette liste, ou `(direct)` |

### 4.2 `item_category` : le tag de parcours ⭐

Les quatre niveaux de catégorie n'ont **pas la même nature** :

- **`item_category2/3/4` = attributs catalogue.** Pour un même `item_id`, ils sont **identiques sur tous les événements et tous les parcours**. Ils décrivent le produit.
- **`item_category` = le tag (attribut de parcours).** Il reflète **le contexte d'affichage d'où le produit a été ajouté au panier** (liste, carrousel, univers du header). Il décrit le parcours, pas le produit.

Règles du tag :

1. **Capture à l'ajout** : la valeur est celle de la liste/carrousel d'où l'utilisateur a ajouté le produit.
2. **Figé par ligne de panier** : la valeur capturée est persistée sur la ligne et rejouée à l'identique sur `view_cart → begin_checkout → add_shipping_info → add_payment_info → purchase`.
3. **`(direct)`** : ajout sans contexte de liste (accès URL directe, ajout depuis la fiche produit, reprise de panier). Dans ce cas `item_list_name` vaut aussi `(direct)` et `item_list_id` est absent.
4. **Deux lignes du même produit peuvent porter deux tags différents** : chaque ligne garde le tag du contexte d'où *elle* a été ajoutée. C'est voulu — cela mesure quel univers de merchandising convertit.

Exemple observé : « Journée Magique Illimitée » ajouté depuis le carrousel *Activités* garde `item_category: "Activités"` jusqu'au bout du tunnel, même lorsqu'il apparaît par ailleurs dans la liste *Billets & Accès* (où le `view_item_list` le montre avec le tag de **cette** liste).

> **Analyse GA4** : utilisez `item_category2/3/4` pour les rapports produit (taxonomie stable), et `item_category` pour analyser la performance des univers de merchandising.

---

## 5. Objet `user`

Présent sur tous les événements quand l'utilisateur est connecté ou identifié.

```javascript
user: {
  user_id:      "CXXXa2296967a1af49cfa3df36ab3d249d1f",
  email_sha256: "dd95e5e0cf238314fd2918b0bc52f17f03e2be22545e8b42da5ac81a9756f041"
}
```

| Champ | Type | Description |
|---|---|---|
| `user_id` | string | Identifiant interne de l'utilisateur dans Qweekle |
| `email_sha256` | string | Hash SHA-256 de l'adresse email (minuscules, sans espaces) |

> Ces champs sont absents si l'utilisateur n'est pas connecté. Les variables GTM retournent `undefined` dans ce cas — aucune donnée utilisateur n'est envoyée aux plateformes.

---

## 6. Règles monétaires : `value`, remises, bons cadeaux, acomptes ⭐

> **Principe fondateur** : la `value` d'un `purchase` représente **la valeur de la commande (le chiffre d'affaires)** — ce que vaut ce qui est vendu — **pas** le montant encaissé en ligne à cet instant.

Chez Qweekle, trois mécanismes réduisent le « montant à payer en ligne » mais ont des sens économiques différents :

| Mécanisme | Nature | Effet sur `value` | Champ |
|---|---|---|---|
| **Code de réduction** (geste commercial) | Vraie remise | **Réduit** `value` | `ecommerce.coupon` (code) + `item.discount` (montant/unité) |
| **Bon cadeau** (avoir prépayé, acheté comme produit `GIFTCARD`) | Moyen de paiement | **N'affecte pas** `value` | `gift_card_amount` (racine, montant utilisé) |
| **Acompte** (paiement partiel en ligne, solde réglé sur place) | Modalité de règlement | **N'affecte pas** `value` | `amount_paid` / `amount_due` (racine) |

Règles :

- `item.price` = prix unitaire **net de réduction** (après `discount`, mais avant bon cadeau/acompte qui ne sont pas des remises).
- `ecommerce.value` = `Σ(price × quantity)` = **valeur de commande**. Identique de `begin_checkout` à `purchase` (panier inchangé). Jamais minorée par un bon cadeau ou un acompte.
- `amount_paid` = montant réellement encaissé en ligne. `amount_due` = solde réglé sur place. `gift_card_amount` = part réglée en bon cadeau.
- Contrôle de cohérence : `amount_paid + amount_due + gift_card_amount = value`.

> Le solde d'un acompte étant réglé **sur place**, GA4 ne le verra jamais autrement : `value` doit porter la commande entière au `purchase`, sinon ce chiffre d'affaires est définitivement perdu.

> **Champ de saisie unique « coupon / bon cadeau »** : l'interface peut proposer un seul champ, mais le dataLayer route selon le type résolu du code — code de réduction → `coupon`/`discount` et `value` minorée ; bon cadeau → `gift_card_amount` et `value` inchangée.

---

## 7. Événement de page : `page_view`

Poussé à chaque navigation réelle (changement de route SPA), avec le contexte de page.

```javascript
{
  event: 'page_view',
  affiliation: 'RE-VOL',
  page_type: 'list',        // home | list | product | account | auth | checkout | confirmation
  page_title: 'RÊVOLUTION - Billets & Accès',
  page_path: '/billets-et-acces',
  user: { user_id: '…', email_sha256: '…' }
}
```

| Champ | Description |
|---|---|
| `affiliation` | Slug du site |
| `page_type` | Type de page — enum fermé : `home`, `list`, `product`, `account`, `auth`, `checkout`, `confirmation` |
| `page_title` / `page_path` | Titre et chemin de la page |

> **Note module GA4** : les modules Qweekle n'exploitent pas cet événement — les pages vues GA4 sont mesurées nativement par la balise Google (All Pages + mesure améliorée SPA). `page_view` reste disponible dans le dataLayer pour les usages avancés (segmentation par `page_type`, autres plateformes).

---

## 8. Événements ecommerce

Chaque événement est précédé d'un push `{ ecommerce: null }`. Tous portent `currency`, `affiliation` et `items` ; `user` est présent si l'utilisateur est identifié.

### `view_item_list` — Affichage d'une liste de produits

Déclenché à l'affichage d'une liste ou d'un carrousel. Les items portent `index` et `item_list_id/name` ; `value` et `quantity` sont absents.

```javascript
{
  event: 'view_item_list',
  ecommerce: {
    currency: 'EUR',
    affiliation: 'RE-VOL',
    item_list_id: 'billets-et-acces',
    item_list_name: 'Billets & Accès',
    items: [
      {
        item_id: 'PXXX…', item_name: 'Abonnement Annuel Rêveur', item_brand: 'RÊVOLUTION',
        item_category: 'Billets & Accès',       // tag = la liste affichée
        item_category2: 'Entrées & Accès', item_category3: 'Passes & Abonnements', item_category4: 'TICKET',
        price: 199, index: 1,
        item_list_id: 'billets-et-acces', item_list_name: 'Billets & Accès'
      }
      // … tous les items visibles de la liste
    ]
  },
  user: { … }
}
```

---

### `view_item` — Affichage d'une fiche produit

`value` = prix du produit. L'item porte le `item_list_id/name` de la liste d'origine si le produit a été atteint depuis une liste.

```javascript
{
  event: 'view_item',
  ecommerce: {
    currency: 'EUR',
    affiliation: 'RE-VOL',
    value: 60,
    items: [ /* 1 item : le produit consulté */ ]
  },
  user: { … }
}
```

---

### `add_to_cart` — Ajout au panier

Contient **tous les produits réellement ajoutés par l'action** (un ajout groupé de N produits ⇒ N entrées dans `items[]`), chacun avec sa `quantity`. `value` = `Σ(price × quantity)` des items ajoutés.

Le tag (`item_category`) et la liste d'origine (`item_list_*`) sont **capturés à cet instant** et resteront figés sur la ligne de panier (voir [section 4.2](#42-item_category--le-tag-de-parcours-)). Ajout depuis la fiche produit ou sans contexte de liste ⇒ `item_category: "(direct)"`.

```javascript
{
  event: 'add_to_cart',
  ecommerce: {
    currency: 'EUR',
    affiliation: 'RE-VOL',
    value: 425,
    items: [
      { item_id: 'PXXX…', item_name: 'Forfait Journée accompagnant', /* … */ price: 55, quantity: 3,
        item_list_id: 'explorez-tous-les-mondes', item_list_name: 'Explorez Tous les Mondes' },
      { item_id: 'PXXX…', item_name: 'Journée Découverte Complète', /* … */ price: 65, quantity: 4,
        item_list_id: 'explorez-tous-les-mondes', item_list_name: 'Explorez Tous les Mondes' }
    ]
  },
  user: { … }
}
```

---

### `remove_from_cart` — Suppression du panier

Même structure que `add_to_cart` : les items retirés, avec leur `quantity`. `value` = somme des lignes retirées.

---

### `view_cart` — Affichage du panier

Tous les items du panier, chaque ligne avec son tag figé. `value` = valeur totale du panier.

> Plusieurs lignes avec le même `item_id` sont **normales et voulues** (une ligne par contexte d'ajout) — ne pas agréger par `item_id`.

---

### `begin_checkout` — Entrée dans le tunnel de commande

Tous les items du panier. `value` = valeur de commande — elle reste identique jusqu'au `purchase`.

```javascript
{
  event: 'begin_checkout',
  ecommerce: {
    currency: 'EUR',
    affiliation: 'RE-VOL',
    value: 1093,
    coupon: 'PROMO10',        // si code de réduction appliqué
    items: [ /* tous les items du panier */ ]
  },
  user: { … }
}
```

---

### `add_shipping_info` — Étape réservation

Émis à la validation de l'étape réservation/retrait du tunnel. Structure identique à `begin_checkout`, plus `shipping_tier`.

```javascript
{
  event: 'add_shipping_info',
  ecommerce: {
    currency: 'EUR',
    affiliation: 'RE-VOL',
    value: 1093,
    shipping_tier: 'Réservation',
    items: [ /* tous les items */ ]
  },
  user: { … }
}
```

---

### `add_payment_info` — Validation du paiement

Émis à la validation des informations de paiement, juste avant la redirection vers le site de paiement. Structure identique, plus `payment_type`.

```javascript
{
  event: 'add_payment_info',
  ecommerce: {
    currency: 'EUR',
    affiliation: 'RE-VOL',
    value: 1093,
    payment_type: 'external',
    items: [ /* tous les items */ ]
  },
  user: { … }
}
```

> **Confirmé en conditions réelles** (capture du 18/09/2026, 3 occurrences) : l'événement est bien émis sur le site marchand, **avant** la redirection vers le domaine de paiement. Il porte l'objet `ecommerce` complet (`value`, `items`, `payment_type: "external"`) et, sur les 3 occurrences observées, l'objet `user`. Le site imposant la connexion avant le paiement, le cas non authentifié n'a pas pu être observé — ne pas supposer qu'il est impossible pour autant.
>
> C'est donc la **dernière étape de tunnel mesurable côté marchand** : le domaine de paiement ne charge pas GTM, et plus aucun événement n'est émis entre ce point et le `purchase` au retour. Utile pour mesurer le taux d'abandon au paiement (`add_payment_info` → `purchase`).

---

### `purchase` — Confirmation de commande

L'événement le plus important. Le paiement s'effectue sur un domaine dédié **sans GTM** : le `purchase` est émis **au retour sur le site de vente**, sur la page de confirmation (`page_type: "confirmation"`), après paiement réussi.

```javascript
{
  event: 'purchase',
  ecommerce: {
    currency:       'EUR',
    affiliation:    'RE-VOL',
    transaction_id: 'OXXX…',        // unique par commande
    value:          1093,           // VALEUR DE COMMANDE (CA) — jamais minorée par bon cadeau/acompte
    tax:            0,
    shipping:       0,
    coupon:         'PROMO10',      // si code de réduction
    payment_type:   'external',
    items: [ /* tous les items, tags figés, prix nets */ ]
  },
  amount_paid:      500,            // montant encaissé en ligne (acompte) — racine
  amount_due:       593,            // solde réglé sur place — racine
  gift_card_amount: 0,              // part réglée en bon cadeau — racine
  user: { user_id: '…', email_sha256: '…' }
}
```

Les trois paramètres monétaires complémentaires sont à la **racine** du push (paramètres custom GA4, hors `ecommerce`) — voir [section 6](#6-règles-monétaires--value-remises-bons-cadeaux-acomptes).

---

## 9. Événements utilisateur

### `login` — Connexion

```javascript
{
  event: 'login',
  user: {
    user_id:      'CXXX…',
    email_sha256: 'dd95e5e0…'
  }
}
```

### `sign_up` — Inscription

```javascript
{
  event: 'sign_up',
  user: {
    user_id:      'CXXX…',
    email_sha256: 'dd95e5e0…'
  }
}
```

### `sign_out` — Déconnexion

```javascript
{
  event: 'sign_out',
  affiliation: 'FU-N',
  user: {
    user_id:      'CXXX…',        // dernier utilisateur connu
    email_sha256: 'dd95e5e0…'
  }
}
```

> L'objet `user` porte encore l'utilisateur **qui vient de se déconnecter**. Ne pas s'en servir pour alimenter un `user_id` après cet événement.

> ⚠️ **Aucun module Qweekle ne consomme `sign_out`** : contrairement à `login` et `sign_up`, il n'existe ni déclencheur ni balise pour cet événement dans les modules livrés. L'événement est bien poussé par la plateforme, mais rien ne le transmet à GA4. Pour le mesurer, créer un déclencheur Custom Event `sign_out` et une balise GA4 sur le modèle de `[GA4] login`.

> `login` et `sign_up` portent aussi `method` (`"email"`) et `affiliation` à la racine.

---

## 10. Notes d'implémentation

**Site de paiement** : le tunnel redirige vers le domaine de paiement `payments.qweekle.app`, qui **ne charge pas GTM**. Aucun événement n'est émis pendant le paiement ; la conversion remonte via le `purchase` au retour sur la page de confirmation du site de vente. Le Conversion Linker Google Ads doit inclure le domaine de paiement dans ses domaines cross-domain pour préserver l'attribution (voir README, section 4.2).

**Déduplication** : chaque `purchase` contient un `transaction_id` unique. Ce champ sert d'`order_id`/`event_id` pour la déduplication entre le Pixel Meta navigateur et l'API Conversions Meta côté serveur, et pour la déduplication des conversions Google Ads. Ne jamais réutiliser un même `transaction_id`.

**Valeurs monétaires** : toutes les valeurs sont en euros, en float (ex : `52.99`). Jamais en centimes.

**Données utilisateur** : `email_sha256` est calculé côté serveur par Qweekle (SHA-256 de l'email en minuscules, sans espaces). Compatible avec Meta Advanced Matching et Google Enhanced Conversions.

**Conteneur mutualisé (optionnel)** : un même conteneur GTM peut être partagé entre plusieurs établissements ; la ségrégation se fait alors par `affiliation`. Dans cette configuration, toute analyse dans GA4 doit filtrer ou segmenter sur ce champ.

---

## 11. Validation terrain (18/09/2026)

Capture Tag Assistant réalisée sur un site de démonstration Qweekle (parc de loisirs), 251 messages, 4 parcours, 3 commandes réellement payées via le PSP.
Source : export Tag Assistant conservé en interne chez Qweekle (non versionné — il contient des identifiants de conteneur, des emails et des commandes réelles).

### 11.1 Événements observés

| Événement | Occurrences | Conforme à cette spec |
|---|---|---|
| `view_item_list` | 11 | Oui |
| `view_item` | 2 | Oui |
| `add_to_cart` | 4 | Oui (jusqu'à 4 lignes en un seul push) |
| `view_cart` | 6 | Oui |
| `begin_checkout` | 3 | Oui |
| `add_payment_info` | 3 | Oui |
| `purchase` | 3 | Oui |
| `login` / `sign_up` / `sign_out` | 1 / 1 / 1 | Oui |
| `page_view` | 21 | Oui (`page_type`, `page_title`, `page_path`) |
| `cookie_consent_update` | 7 | Non documenté ici — événement CMP, voir README |
| `remove_from_cart`, `add_shipping_info` | 0 | Non observés (non joués dans ces parcours) |

### 11.2 Champs jamais observés sur ce site

Ces champs sont spécifiés mais **absents de la totalité de la capture**. Les variables GTM correspondantes existent dans les templates et renvoient `undefined` — sans effet négatif, mais rien ne remonte.

| Champ | Statut |
|---|---|
| `amount_due` | Jamais poussé — aucun acompte sur ce site (paiement toujours intégral) |
| `gift_card_amount` | Jamais poussé — aucun bon cadeau utilisé pendant les tests |
| `ecommerce.coupon` / `item.discount` | Jamais poussés — aucun code de réduction testé |
| `ecommerce.shipping_tier` | Jamais poussé — cohérent, pas de livraison |
| `item_variant` | Jamais poussé |

> `amount_paid` **est** présent sur les 3 `purchase` et vaut exactement `ecommerce.value` (100 / 120 / 50). Le contrôle `amount_paid + amount_due + gift_card_amount = value` de la [section 6](#6-règles-monétaires--value-remises-bons-cadeaux-acomptes) est donc vérifié dans le cas simple, mais **le cas acompte reste non testé à ce jour**.

### 11.3 Écarts constatés

**1. `user` absent sur `begin_checkout` en visiteur non connecté.**
Le site n'autorise pas le guest checkout, mais `begin_checkout` se déclenche **avant** la redirection vers `/auth/login`. Sur les 3 `begin_checkout` observés, 1 est parti sans objet `user`. Idem pour `add_to_cart` / `view_cart` en session anonyme.
→ Toute variable ou tag supposant la présence de `user` doit tolérer son absence. C'est déjà le comportement des templates (variables `undefined`), mais à garder en tête pour les segments et l'Enhanced Conversions.

**2. `{ ecommerce: null }` non poussé avant `view_cart` quand il suit immédiatement `add_to_cart`.**
Observé 3 fois sur 6 `view_cart`. Sans conséquence ici car `view_cart` re-pousse un objet `ecommerce` complet (currency, value, items) qui écrase intégralement le précédent — aucune donnée résiduelle ne fuit. À corriger côté plateforme pour la conformité stricte à la [section 8](#8-événements-ecommerce), sans urgence.

**3. Pas de `view_item` sur les produits « achat rapide ».**
Les produits de la Billetterie s'achètent depuis la liste, sans fiche produit : ils génèrent `view_item_list` puis directement `add_to_cart`. Seuls les produits à configurateur (Trampoline, Plaine de jeux) émettent `view_item`.
→ Conséquence directe : les tags déclenchés sur `view_item` (`[Meta] ViewContent`, `[Google Ads] Remarketing`) ne couvrent **pas** la Billetterie. Sur cette capture, ils n'ont fait que 2 déclenchements chacun.

**4. Aucun signal d'abandon de panier.**
Ni `remove_from_cart`, ni événement de sortie de tunnel. Pour le remarketing panier abandonné, seul le dernier couple `add_to_cart` / `view_cart` est exploitable.

**5. Site en SPA.**
La navigation interne émet `gtm.historyChange-v2` (35 occurrences) sans rechargement. Un déclencheur « All Pages » seul ne se redéclenche pas en navigation interne — c'est voulu pour la balise de configuration GA4, mais à connaître pour tout tag de page vue.
