# UML - Final Versions

---

# Exo 1 - Hospital Management System

## Class diagram

```mermaid
classDiagram
    class User {
        <<abstract>>
        #int id
        #String name
        #String passwordHash
        +login()
        +logout()
    }
    class Patient {
        -String address
        +postProblem()
        +pay()
    }
    class Doctor {
        -String speciality
        +writePrescription()
    }
    class Organizer {
        +consultDoctor()
        +sendPrescription()
        +forwardPayment()
        +createMember()
        +updateSystem()
    }
    class HealthProblem {
        -int id
        -String description
        -Date createdAt
        -Date updatedAt
        -ProblemStatus status
        +changeStatus()
    }
    class ProblemStatus {
        <<enumeration>>
        PENDING
        IN_REVIEW
        RESOLVED
    }
    class Consultation {
        -Date date
        -String notes
    }
    class Prescription {
        -int id
        -String content
        -Date issuedAt
        -double price
    }
    class Payment {
        <<abstract>>
        -int id
        -double amount
        -Date date
        -PaymentStatus status
        +process()*
    }
    class PaymentStatus {
        <<enumeration>>
        PENDING
        PAID
        FORWARDED
    }
    class Check
    class Cash
    class CreditCard

    User <|-- Patient
    User <|-- Doctor
    User <|-- Organizer
    Patient "1" --> "0..*" HealthProblem : posts
    HealthProblem --> ProblemStatus
    HealthProblem "1" -- "0..*" Consultation
    Doctor "1" -- "0..*" Consultation
    Consultation "1" --> "0..1" Prescription : produces
    Patient "1" --> "0..*" Prescription : history
    Prescription "1" --> "0..1" Payment
    Payment --> PaymentStatus
    Payment <|-- Check
    Payment <|-- Cash
    Payment <|-- CreditCard
```

## SSD 1 - Patient registration

```mermaid
sequenceDiagram
    actor Pa as Patient
    actor O as Organizer
    participant S as System

    Pa->>O: request membership (personal info)
    O->>S: createMember(info)
    S->>S: generate id + password
    S-->>O: member created (id, password)
    O-->>Pa: send credentials
```

## SSD 2 - Consultation flow

```mermaid
sequenceDiagram
    actor Pa as Patient
    participant S as System
    actor O as Organizer
    actor D as Doctor

    Pa->>S: login()
    Pa->>S: postProblem(description)
    S-->>Pa: status = PENDING
    O->>S: getPendingProblems()
    S-->>O: list of problems
    O->>S: assignDoctor(problem, doctor)
    S->>S: status = IN_REVIEW
    D->>S: writePrescription(problem, content)
    S->>S: status = RESOLVED
    O->>S: sendPrescription(problem)
    S-->>Pa: prescription available
```

## SSD 3 - Payment processing

```mermaid
sequenceDiagram
    actor Pa as Patient
    participant S as System
    actor O as Organizer
    actor D as Doctor

    Pa->>S: pay(prescription, method)
    alt Check or Cash
        S->>S: record payment (PENDING)
        O->>S: confirmReceipt(payment)
    else CreditCard
        S->>S: charge card
    end
    S->>S: status = PAID
    S-->>Pa: receipt
    O->>S: forwardPayment(payment, doctor)
    S->>S: status = FORWARDED
    S-->>D: payment notification
```

---

# Exo 2 - ABCD Records

## Use case diagram

```mermaid
flowchart LR
    NM([Non-Member])
    M([Member])
    RM([Royal Member])
    OPC([Order Processing Clerk])
    CDC([Collection Dept Clerk])

    subgraph System["ABCD Records System"]
        Send((Send Membership Application))
        Place((Place Order))
        Verify((Verify Membership))
        Avail((Verify Item Availability))
        Process((Process Order))
        Disc((Apply Discount))
        Unavail((Order Unavailable Items))
        Inv((Print Invoice))
        Ship((Print Shipping List))
        Pay((Make Payment))
        Collect((Handle Payment))
    end

    NM --- Send
    M --- Place
    M --- Pay
    RM --- Place
    OPC --- Process
    OPC --- Verify
    CDC --- Collect

    Place -. "include" .-> Verify
    Place -. "include" .-> Avail
    Process -. "include" .-> Inv
    Process -. "include" .-> Ship
    Disc -. "extend (Royal only)" .-> Place
    Unavail -. "extend (unavailable, Royal only)" .-> Place
    Collect -. "include" .-> Pay
```

## Class diagram

```mermaid
classDiagram
    class Member {
        <<abstract>>
        -int memberId
        -String name
        -String address
        +placeOrder()
        +makePayment()
    }
    class RoyalMember {
        -double discountRate
        +orderUnavailableItem()
    }
    class RegularMember
    class NonMember {
        +requestApplication()
    }
    class MembershipApplication {
        -int id
        -Date date
        -String status
    }
    class Order {
        -int orderId
        -Date date
        -String status
        +addLine()
        +calculateTotal()
    }
    class OrderLine {
        -int quantity
        -double unitPrice
        -boolean backordered
    }
    class Item {
        <<abstract>>
        -int itemId
        -String title
        -double price
        -int stock
        +isAvailable()
    }
    class CD
    class Tape
    class Invoice {
        -int invoiceNo
        -Date date
        -double total
        +print()
    }
    class ShippingList {
        -int listNo
        -Date date
        +print()
    }
    class Payment {
        <<abstract>>
        -int id
        -double amount
        -Date date
        +process()*
    }
    class Cash
    class Check {
        -String checkNumber
    }
    class BankDraft {
        -String draftNumber
    }
    class OrderProcessingClerk {
        +verifyMembership()
        +processOrder()
    }
    class CollectionClerk {
        +handlePayment()
    }

    Member <|-- RoyalMember
    Member <|-- RegularMember
    Item <|-- CD
    Item <|-- Tape
    Payment <|-- Cash
    Payment <|-- Check
    Payment <|-- BankDraft

    Member "1" --> "0..*" Order : places
    Order "1" *-- "1..*" OrderLine : contains
    OrderLine "0..*" --> "1" Item : refers to
    Order "1" --> "1" Invoice : generates
    Order "1" --> "0..1" ShippingList : generates
    Order "1" --> "0..*" Payment : paid by
    OrderProcessingClerk "1" --> "0..*" Order : processes
    CollectionClerk "1" --> "0..*" Payment : handles
    NonMember "1" --> "0..*" MembershipApplication : receives
```

## Sequence 1 - Complete order processing

```mermaid
sequenceDiagram
    actor M as Member
    participant S as System
    actor C as Order Processing Clerk
    actor CC as Collection Clerk

    M->>S: placeOrder(items)
    S->>C: verifyMembership(member)
    C-->>S: valid
    loop each OrderLine
        S->>S: checkAvailability(item)
    end
    S->>S: applyDiscount (if Royal)
    S->>C: processOrder(order)
    C->>S: printInvoice()
    C->>S: printShippingList()
    S-->>M: invoice
    M->>CC: pay(amount, method)
    CC->>S: recordPayment()
    S->>S: save to daily records file
```

## Sequence 2 - Membership verification

```mermaid
sequenceDiagram
    actor U as Customer
    participant S as System
    actor C as Order Processing Clerk

    U->>S: placeOrder()
    S->>C: verifyMembership(id)
    alt member found
        C-->>S: valid (Regular or Royal)
        S-->>U: order accepted
    else not a member
        C-->>S: invalid
        S-->>U: send membership application form
    end
```

## Sequence 3 - Payment processing

```mermaid
sequenceDiagram
    actor M as Member
    actor CC as Collection Clerk
    participant S as System

    M->>CC: pay(order, method)
    alt Cash
        CC->>S: recordCash(amount)
    else Check
        CC->>S: recordCheck(checkNumber)
        S->>S: wait for clearing
    else Bank Draft
        CC->>S: recordDraft(draftNumber)
    end
    S->>S: mark order PAID
    S-->>M: receipt
```

## Sequence 4 - Item reordering for Royal members

```mermaid
sequenceDiagram
    actor R as Royal Member
    participant S as System
    actor C as Order Processing Clerk

    R->>S: placeOrder(item)
    S->>S: checkAvailability(item)
    alt item available
        S-->>R: order confirmed
    else unavailable
        alt member is Royal
            S->>S: create backorder line
            S->>C: reorder(item) from supplier
            S-->>R: order accepted, item backordered
        else Regular member
            S-->>R: item unavailable
        end
    end
```
