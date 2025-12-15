import string
from models import TutorProfile

# Optional keyword mapping for fuzzy matching
MAJOR_KEYWORDS = {
    "computer science": ["data", "programming", "statistical", "modeling", "ai", "ml"],
    "economics": ["finance", "markets", "economics", "global"],
    "english": ["literature", "writing", "reading", "creative"],
    "biology": ["biology", "ecology", "evolution", "neuroscience"],
    # add more as needed
}

STOPWORDS = {"and", "or", "the", "of", "in", "a", "an"}

def normalize_text(text):
    """Lowercase, remove punctuation, split into words."""
    if not text:
        return set()
    return set(
        word for word in text.lower().translate(str.maketrans("", "", string.punctuation)).split()
        if word not in STOPWORDS
    )

def generate_suggested_matches(tutor_request, top_n=4):
    matches = []

    # Normalize requested majors from form
    requested_majors = set(
        m.strip().lower() for m in (tutor_request.majors or "").split(",") if m.strip()
    )

    tutors = TutorProfile.query.filter_by(active=True).all()

    print(f"\nGenerating matches for request ID {tutor_request.id}: '{tutor_request.courseName}'")
    print(f"Requested majors: {requested_majors}")
    print(f"Found {len(tutors)} active tutors\n")

    for tutor in tutors:
        score = 0
        reasons = []

        print(f"Checking tutor: {tutor.name} (ID {tutor.id})")

        # Requested tutor match
        if tutor_request.requestedTutorId and tutor.id == tutor_request.requestedTutorId:
            score += 100
            reasons.append("Requested tutor")

        # Tutor majors normalized
        tutor_majors = set(m.strip().lower() for m in tutor.majors.split(",") if m.strip())

        # Major match from form (priority)
        major_matches = tutor_majors & requested_majors
        if major_matches:
            score += 50
            reasons.append(f"Major match ({', '.join(major_matches)})")

        # Fallback: keyword match from course description if no major match
        if not major_matches:
            course_words = normalize_text(tutor_request.courseName + " " + tutor_request.courseDescription)
            for major in tutor_majors:
                keywords = MAJOR_KEYWORDS.get(major, [])
                if major in course_words or any(k in course_words for k in keywords):
                    score += 20  # smaller weight for fallback
                    reasons.append(f"Keyword match ({major})")
                    break

        # Language match
        tutor_languages = normalize_text(tutor.languages)
        course_words = normalize_text(tutor_request.courseName + " " + tutor_request.courseDescription)
        lang_matches = tutor_languages & course_words
        if lang_matches:
            score += 30
            reasons.append(f"Language match ({', '.join(lang_matches)})")

        # Interests match
        tutor_interests = normalize_text(tutor.interests)
        interest_matches = tutor_interests & course_words
        if interest_matches:
            score += 20
            reasons.append(f"Interest match ({', '.join(interest_matches)})")

        if score > 0:
            matches.append({
                "tutorId": tutor.id,
                "tutorName": tutor.name,
                "score": score,
                "reason": ", ".join(reasons)
            })
            print(f"Tutor '{tutor.name}' matched! Score: {score}, Reasons: {', '.join(reasons)}")
        else:
            print(f"Tutor '{tutor.name}' has no matches")

    # Sort descending by score and return top_n
    matches.sort(key=lambda x: x["score"], reverse=True)
    print(f"\nTop {top_n} matches: {matches[:top_n]}\n")
    return matches[:top_n]
