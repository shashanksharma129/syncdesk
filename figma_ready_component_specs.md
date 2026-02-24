Perfect timing. Below are **Figma‑ready component specifications** that a designer (or you) can directly translate into frames, components, variants, and auto‑layout rules.

This is **not vague design advice** — it’s a **systematic component contract** aligned with:
- The frozen V1 spec  
- Mobile‑first constraints (Etawah reality)
- Calm, professional school UX  
- Frontend + backend behavior

You can paste this into:
- A Figma page as documentation, **or**
- Hand it to a designer and say “design exactly this”

---

# 🎨 Figma‑Ready Component Specs  
**School Communication & Helpdesk OS — V1**

---

## 0. Global Design Foundations (Figma Setup)

### Frame Sizes (Mobile‑First)
- **Primary**: 360 × 800 (Android baseline)
- Tablet/Desktop: Optional later

### Grid
- 8px spacing system
- Max content width: 360px
- Side padding: 16px

---

## 1. Color System (Professional & Calm)

### Core Colors
- Primary: `#1F3A5F` (Navy blue – trust)
- Secondary: `#4C6EF5` (Action blue)
- Background: `#F8FAFC`
- Surface: `#FFFFFF`
- Border: `#E5E7EB`
- Text Primary: `#111827`
- Text Secondary: `#6B7280`

### Status Colors
| Status | Color | Usage |
|---|---|---|
| Pending | `#F59E0B` | Badge, subtle |
| In Progress | `#2563EB` | Badge |
| Resolved | `#16A34A` | Badge |
| Urgent | `#DC2626` | Icon + badge |

❗ No red text blocks. Red only as indicator.

---

## 2. Typography

### Font
- Inter (or system fallback)

### Type Scale
| Style | Size | Weight |
|---|---|---|
| Page Title | 20 | Semibold |
| Section Title | 16 | Semibold |
| Body | 14 | Regular |
| Caption | 12 | Regular |
| Button | 14 | Medium |

Line height: 1.4–1.6×

---

## 3. Core UI Primitives (Figma Components)

---

### 3.1 Button

**Component:** `Button`

**Variants**
- Primary
- Secondary
- Ghost
- Disabled

**Sizes**
- Default: height 44px
- Full width on mobile

**States**
- Default
- Pressed
- Loading (spinner, text hidden)
- Disabled

✅ Use auto‑layout  
✅ Rounded: 8px  
✅ Touch‑friendly

---

### 3.2 Input Field

**Component:** `InputField`

**Structure**
- Label (required)
- Input box
- Helper text / error text

**States**
- Default
- Focused
- Error
- Disabled

**Rules**
- Label always visible (no floating labels)
- Error text in muted red, calm language

---

### 3.3 Select / Dropdown

**Component:** `SelectField`

**Behavior**
- Opens bottom sheet on mobile
- Shows selected value
- Multi‑select variant supported

---

### 3.4 Textarea

Same as InputField, but:
- Min height: 96px
- Auto expand optional

---

### 3.5 Badge

**Component:** `StatusBadge`

**Variants**
- Pending
- In Progress
- Resolved
- Urgent

Rounded pill, subtle background.

---

### 3.6 Alert / Banner

**Component:** `InfoBanner`

**Variants**
- Info
- Warning
- Error

**Usage**
- Guardrails
- Office hours
- Admin notices

✅ Calm tone  
✅ Icon + text  
✅ Dismissible (optional)

---

## 4. Navigation Components

---

### 4.1 Top Header

**Component:** `TopHeader`

**Contents**
- School name
- Optional role indicator

Sticky at top.

---

### 4.2 Bottom Navigation (Mobile)

**Component:** `BottomNav`

**Items**
- Home
- Tickets
- Announcements
- Profile

Icons + labels  
Active state highlighted.

---

## 5. Domain Components (Core Screens)

---

### 5.1 Ticket Card

**Component:** `TicketCard`

**Contents**
- Category
- Status badge
- Child name(s)
- Last updated time
- Urgent indicator (if any)

**Behavior**
- Entire card clickable
- Elevation on press

---

### 5.2 Ticket Thread Message

**Component:** `MessageBubble`

**Variants**
- Parent
- Staff

**Rules**
- Parent: right‑aligned, light background
- Staff: left‑aligned, neutral background
- Timestamp (caption size)

---

### 5.3 Internal Note (Staff‑Only)

**Component:** `InternalNoteBox`

**Visual**
- Light yellow background
- Lock icon
- Text:
  > “Internal notes are part of permanent records.”

Never rendered for parents.

---

### 5.4 Ticket Status Header

**Component:** `TicketStatusHeader`

**Contents**
- Category
- Status badge
- Assigned role

Prominent but calm.

---

## 6. Ticket Creation Flow Components

---

### 6.1 Student Selector

**Component:** `StudentSelector`

**Variants**
- Single
- Multi‑select

**Rules**
- Mandatory selection
- Selected students shown as chips

---

### 6.2 Confirmation Panel

**Component:** `ConfirmationPanel`

**Text**
> “This ticket is about: Child A, Child B”

Used before submit.

---

### 6.3 Guardrail Error Banner

**Component:** `GuardrailBanner`

**Examples**
- “You already have 3 open requests.”
- “You can create a new request in 18 minutes.”

No blame language.

---

## 7. Announcements Components

---

### 7.1 Announcement Card

**Component:** `AnnouncementCard`

**Contents**
- Title
- Date
- Attachment icon (if any)

Unread announcements subtly highlighted.

---

### 7.2 Announcement Detail

**Component:** `AnnouncementDetail`

**Contents**
- Full text
- Attachment download
- No reply UI

---

## 8. Staff‑Specific Components

---

### 8.1 Ticket Inbox Row

**Component:** `InboxRow`

**Contents**
- Ticket summary
- Urgency indicator
- Time open

---

### 8.2 Status Update Control

**Component:** `StatusDropdown`

**Options**
- Pending
- In Progress
- Resolved

Requires confirmation.

---

### 8.3 Reopen Prompt (Parent)

**Component:** `ReopenPrompt`

**Options**
- ✅ Resolved
- ❌ Request Reopen (textarea appears)

---

## 9. Transport‑Specific Components

---

### 9.1 Known Issue Banner

**Component:** `KnownIssueBanner`

Text:
> “This is a known transport issue. Updates will be shared.”

---

### 9.2 Broadcast Update Panel

**Component:** `BroadcastPanel`

**Fields**
- Route selector
- Message (readonly template)
- Send button

Footer (fixed):
> “No action required from parents.”

---

## 10. Notifications UI

---

### 10.1 Notification Item

**Component:** `NotificationItem`

**Contents**
- Icon
- Message
- Timestamp
- Read/unread state

Clickable → deep link.

---

## 11. Empty States (Very Important)

**Component:** `EmptyState`

**Structure**
- Icon
- Calm message
- Optional CTA

Examples:
- “No tickets yet”
- “No announcements today”

---

## 12. Accessibility & UX Rules (Global)

- Minimum tap target: 44px
- No color‑only meaning
- All forms have labels
- Loading states everywhere
- No sudden screen jumps

---

## ✅ Final Notes for Figma

In Figma:
- Use **Auto Layout everywhere**
- Use **Variants**, not duplicate components
- Name components clearly:
  - `Button / Primary`
  - `Badge / Resolved`
- Create a **“Do Not Use”** section for deprecated styles

---
