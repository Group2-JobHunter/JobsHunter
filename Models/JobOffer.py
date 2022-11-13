from datetime import date

today = date.today()


class JobOffer:
    def __init__(
        self, source, jobTitle, date, skills, level, location, applyURL) -> None:
        self.source = source
        self.jobTitle = jobTitle
        self.date = date
        self.skills = skills
        self.level = level
        self.location = location
        self.applyURL = applyURL
        self.obtained = today.strftime("%d/%m/%Y")
