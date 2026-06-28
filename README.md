# CampusCrew Web App

## Setup karo
```bash
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

## Flow
1. `/register/` — Account + Profile banao
2. `/join/` — Team choose karo (Tech / Marketing / Accommodation)  
3. Apply form fill karo (photo upload karo)
4. Crew ID + Referral Code milega (same code)
5. `/dashboard/` — Apna ID card, stats & top 3 performers dekho

## Admin
`/admin/` pe `reward_points` update karo to populate leaderboard.

## Crew ID Format
- Tech Team: `CC-TECH-XXXXX`
- Marketing: `CC-MKT-XXXXX`  
- Accommodation: `CC-ACC-XXXXX`
