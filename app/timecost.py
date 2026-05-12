from datetime import date, timedelta
from app import db
from app.models import Settings, TimerSession, User

def get_date_range(period):
    today = date.today()
    if period == 'week':
        start_date = today - timedelta(days=today.weekday())  # Monday
        end_date = today

    elif period == 'month':
        start_date = today.replace(day=1)  # First day of the month
        end_date = today

    elif period == 'day':
        start_date = today
        end_date = today
    else:
        raise ValueError("Invalid period. Use 'week', 'month', or 'day'.")

    return start_date.isoformat(), end_date.isoformat()

def get_leaderboard(period):
    start_date, end_date = get_date_range(period)
    
    totals = (
        db.session.query(
            TimerSession.user_id.label('user_id'),
            db.func.sum(TimerSession.timeCost).label('total_time')
        )
        .filter(
            TimerSession.sessiondate >= start_date,
            TimerSession.sessiondate <= end_date
        )
        .group_by(TimerSession.user_id)
        .subquery()
    )

    rows = (
        db.session.query(
            User.id,
            User.nickname,
            User.avatar,
            db.func.coalesce(totals.c.total_time, 0).label('total_time')
        )
        .outerjoin(totals, User.id == totals.c.user_id)
        .outerjoin(Settings, User.id == Settings.id)
        .filter(db.or_(Settings.id.is_(None), Settings.show_leaderboard.is_(True)))
        .order_by(db.desc('total_time'))
        .all()
    )

    return rows
