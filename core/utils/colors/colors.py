from sqlalchemy.orm import Session
from models.tags import TagDB

TAG_COLORS = [
    # Royal Purple
    "#bc93ed",
    "#a16ae2",
    "#8b4ad3",
    "#7638b8",
    "#663399",
    "#371358",  
    # FIN - Royal Purple
    "#ef4444",  # red-500
    "#f97316",  # orange-500
    "#f59e0b",  # amber-500
    "#eab308",  # yellow-500
    "#84cc16",  # lime-500
    "#22c55e",  # green-500
    "#10b981",  # emerald-500
    "#14b8a6",  # teal-500
    "#06b6d4",  # cyan-500
    "#0ea5e9",  # sky-500
    "#3b82f6",  # blue-500
    "#6366f1",  # indigo-500
    "#8b5cf6",  # violet-500
    "#a855f7",  # purple-500
    "#  ",  # pink-500
    "#f43f5e",  # rose-500
    "#6b7280",  # gray-500 (único gris permitido)
]


def get_next_available_color(db: Session) -> str:
    used_colors = {tag.color for tag in db.query(TagDB.color).distinct()}
    for color in TAG_COLORS:
        if color not in used_colors:
            return color
    # Si todos están en uso, repite el ciclo
    return TAG_COLORS[len(used_colors) % len(TAG_COLORS)]

def validate_color(color:str) -> str:
    pass