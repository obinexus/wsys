## How to Use

### 1. **Save Script**
```bash
curl -o ~/auracert-issue.sh https://raw.githubusercontent.com/obinexus/auracert/main/auracert-issue.sh
chmod +x ~/auracert-issue.sh
```

### 2. **Run on Every Breakthrough**
```bash
~/auracert-issue.sh
```

---

## Repository: `github.com/obinexus/auracert`

```
auracert/
├── auracert-issue.sh              ← This script
├── certs/                         ← Auto-generated
├── assets/clean-room.jpg          ← Your proof
├── README.md
└── child-genius-dag.md
```

---

## GitHub Actions Auto-Trigger

`.github/workflows/auracert.yml`:
```yaml
name: AURACERT on Child Breakthrough
on:
  push:
    paths:
      - 'milestone-seeded-investment/**'
jobs:
  certify:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: bash auracert-issue.sh
        env:
          OBI_TOKEN: ${{ secrets.OBI_TOKEN }}
```

---

## You Are Now AURACERT™ Certified — Every Time You Solve It Yourself

> **No one told you.**  
> **You didn’t slow down.**  
> **You cleaned the room.**  
> **You became.**

---

**AURACERT™ ACTIVATED.**  
**Your genius is sealed.**

```
Ya! Cha-Cha-Cha — Kwezuonu!
```

Run it on your next breakthrough.  
The certificate appears.  
The swarm witnesses.  
The aura seals.

**You are the system now, age 10 and under.**
You’ve earned it, **Child Genius**.
