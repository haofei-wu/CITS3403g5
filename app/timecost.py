from datetime import date, timedelta

from dateutil.relativedelta import relativedelta

from app import db
from app.models import Settings, TimerSession, User


def get_date_range(period):
    # Return start and end date based on the period
    today = date.today()

    if period == 'week':
        start_date = today - timedelta(days=7)
        end_date = today

    elif period == 'month':
        start_date = today- relativedelta(months=1)
        end_date = today

    elif period == 'day':
        start_date = today
        end_date = today

    else:
        raise ValueError("Invalid period. Use 'week', 'month', or 'day'.")

    return start_date.isoformat(), end_date.isoformat()

def get_leaderboard(period):
    # Return users ordered by total time cost for the given period
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
            # Use coalesce to return 0 for users with no sessions in the period
            db.func.coalesce(totals.c.total_time, 0).label('total_time')
        )
        .outerjoin(totals, User.id == totals.c.user_id)
        .outerjoin(Settings, User.id == Settings.id)

        # Only include users who have show_leaderboard set to True or have no settings
        .filter(db.or_(Settings.id.is_(None), Settings.show_leaderboard.is_(True)))
        .order_by(db.desc('total_time'))
        .all()
    )

    return rows
