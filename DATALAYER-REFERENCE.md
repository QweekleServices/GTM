# Référence DataLayer — Qweekle

> **Audience** : agences marketing et intégrateurs techniques
> Document complémentaire à [README.md](README.md)

Ce document décrit l'ensemble des événements poussés par la plateforme Qweekle dans le `dataLayer`, leur structure de données et les valeurs attendues.

---

## Table des matières

1. [Structure générale](#1-structure-générale)
2. [Objet `ecommerce`](#2-objet-ecommerce)
3. [Objet `user`](#3-objet-user)
4. [Événements ecommerce](#4-événements-ecommerce)
5. [Événements utilisateur](#5-événements-utilisateur)
6. [Événements de navigation](#6-événements-de-navigation)
7. [Champs contextuels](#7-champs-contextuels)
8. [Valeurs de référence](#8-valeurs-de-référence)

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

---

## 2. Objet `ecommerce`

### Structure complète

```javascript
ecommerce: {
  currency:       "EUR",
  value:          52.99,           // montant en euros (float)
  transaction_id: "CMD-20260313-001", // unique par commande (événement purchase uniquement)
  coupon:         "PROMO10",       // code promo appliqué (optionnel)
  items: [
    {
      item_id:   "SKU-123",
      item_name: "Nom du produit",
      price:     25.99,
      quantity:  2,
      item_category: "Tag", // Tag (catégorie en ligne) du produit
      item_category_2: "Catégorie", // Catégorie dans le catalogue produit
      item_category_3: "Sous-Catégorie", // Sous-Catégorie dans le catalogue produit
      item_category_4: "Type", // Type de produit
    }
  ]
}
```

### Détail des champs

| Champ | Type | Toujours présent | Description |
|---|---|---|---|
| `currency` | string | ✅ | Code devise ISO 4217. Valeur fixe : `EUR` |
| `value` | float | ✅ | Valeur monétaire de l'événement en euros |
| `transaction_id` | string | Purchase uniquement | Identifiant unique de la commande |
| `coupon` | string | Non | Code promo appliqué à la commande |
| `items` | array | ✅ | Tableau des produits concernés (voir ci-dessous) |

### Champs d'un item

| Champ | Type | Toujours présent | Description |
|---|---|---|---|
| `item_id` | string | ✅ | Identifiant unique du produit (SKU) |
| `item_name` | string | ✅ | Nom du produit |
| `price` | float | ✅ | Prix unitaire en euros |
| `quantity` | integer | ✅ | Quantité |
| `item_category` | string | Non | Tag (catégorie en ligne) du produit |
| `item_category_2` | string | Non | Catégorie dans le catalogue produit |
| `item_category_3` | string | Non | Sous-Catégorie dans le catalogue produit |
| `item_category_4` | string | Non | Type de produit |
---

## 3. Objet `user`

Présent sur tous les événements quand l'utilisateur est connecté ou identifié.

```javascript
user: {
  user_id:      "usr_12345",
  email_sha256: "a665a45920422f9d417e4867efdc4fb8a04a1f3fff1fa07e998e86f7f7a27ae3"
}
```

| Champ | Type | Description |
|---|---|---|
| `user_id` | string | Identifiant interne de l'utilisateur dans Qweekle |
| `email_sha256` | string | Hash SHA-256 de l'adresse email (minuscules, sans espaces) |

> Ces champs sont absents si l'utilisateur n'est pas connecté. Les variables GTM retournent `undefined` dans ce cas — aucune donnée utilisateur n'est envoyée aux plateformes.

---

## 4. Événements ecommerce

### `view_item_list` — Affichage d'une liste de produits

Déclenché lors de l'affichage d'une page de catalogue ou d'un résultat de collection.

```javascript
{
  event: 'view_item_list',
  ecommerce: {
    currency: 'EUR',
    items: [ /* produits visibles */ ]
  },
  navigation_context: 'list'
}
```

---

### `select_item` — Clic sur un produit

Déclenché quand l'utilisateur clique sur un produit dans une liste.

```javascript
{
  event: 'select_item',
  ecommerce: {
    currency: 'EUR',
    items: [ /* produit sélectionné */ ]
  },
  navigation_context: 'list'
}
```

---

### `view_item` — Affichage d'une fiche produit

Déclenché à l'ouverture d'une page produit.

```javascript
{
  event: 'view_item',
  ecommerce: {
    currency: 'EUR',
    value:    25.99,
    items: [ /* produit consulté */ ]
  },
  navigation_context: 'product'
}
```

---

### `add_to_cart` — Ajout au panier

```javascript
{
  event: 'add_to_cart',
  ecommerce: {
    currency: 'EUR',
    value:    25.99,
    items: [ /* produit ajouté */ ]
  }
}
```

---

### `remove_from_cart` — Suppression du panier

```javascript
{
  event: 'remove_from_cart',
  ecommerce: {
    currency: 'EUR',
    value:    25.99,
    items: [ /* produit supprimé */ ]
  }
}
```

---

### `view_cart` — Affichage du panier

```javascript
{
  event: 'view_cart',
  ecommerce: {
    currency: 'EUR',
    value:    75.98,
    items: [ /* tous les produits du panier */ ]
  }
}
```

---

### `begin_checkout` — Début de tunnel de commande

```javascript
{
  event: 'begin_checkout',
  ecommerce: {
    currency: 'EUR',
    value:    75.98,
    coupon:   'PROMO10',   // si code promo appliqué
    items: [ /* produits du panier */ ]
  },
  checkout_type: 'guest'   // 'guest' | 'login' | 'signup'
}

---

### `purchase` — Confirmation de commande

Événement le plus important. Déclenché sur la page de confirmation après paiement réussi.

```javascript
{
  event: 'purchase',
  ecommerce: {
    currency:       'EUR',
    value:          75.98,
    transaction_id: 'CMD-20260313-001',
    coupon:         'PROMO10',
    payment_type:   'card',
    items: [
      { item_id: 'SKU-123', item_name: 'Produit A', price: 25.99, quantity: 2 },
      { item_id: 'SKU-456', item_name: 'Produit B', price: 24.00, quantity: 1 }
    ]
  },
  user: {
    user_id:      'usr_12345',
    email_sha256: 'a665a45920...'
  },
  payment_type:   'card',
  checkout_type:  'login'
}
```

---

## 5. Événements utilisateur

### `login` — Connexion

```javascript
{
  event: 'login',
  user: {
    user_id:      'usr_12345',
    email_sha256: 'a665a45920...'
  }
}
```

### `sign_up` — Inscription

```javascript
{
  event: 'sign_up',
  user: {
    user_id:      'usr_12345',
    email_sha256: 'a665a45920...'
  }
}
```

---

## 6. Événements de navigation

### `search` — Recherche

```javascript
{
  event: 'search',
  search_term: 'robe noire'
}
```

---

## 7. Champs contextuels

Ces champs apparaissent sur certains événements pour enrichir le contexte.

| Champ | Événements | Description |
|---|---|---|
| `navigation_context` | `view_item_list`, `select_item`, `view_item` | Contexte de la navigation au moment de l'événement |
| `checkout_type` | `begin_checkout`, `purchase` | Type de tunnel emprunté |
| `payment_type` | `add_payment_info`, `purchase` | Mode de paiement utilisé |
| `search_term` | `search` | Terme saisi dans le moteur de recherche interne |

---

## Notes d'implémentation

**Déduplication** : chaque événement `purchase` contient un `transaction_id` unique. Ce champ est utilisé comme `event_id` pour la déduplication entre le Pixel Meta navigateur et l'API Conversions Meta côté serveur. Ne jamais réutiliser un même `transaction_id`.

**Valeurs monétaires** : toutes les valeurs sont en euros, en float (ex : `52.99`). Jamais en centimes. GTM et les plateformes reçoivent directement la valeur en euros.

**Données utilisateur** : le champ `email_sha256` est calculé côté serveur par Qweekle. L'algorithme appliqué est SHA-256 sur l'adresse email en minuscules, sans espaces avant ou après. Compatible avec les exigences de Meta Advanced Matching et Google Enhanced Conversions.
