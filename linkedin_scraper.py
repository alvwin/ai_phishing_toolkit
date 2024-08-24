import getpass
from linkedin_api import Linkedin
import configparser
import requests

# Load LinkedIn login info from config file
def load_login_info():
      config = configparser.ConfigParser()
      config.read('config.ini')
      try:
            uname = config.get('linkedin', 'username')
            passwd = config.get('linkedin', 'password')
      except (configparser.NoSectionError, configparser.NoOptionError):
            print("LinkedIn login info not found in config file.")
            uname = input("Please enter your username: ")
            passwd = getpass.getpass("Please enter your password: ")
            if not config.has_section('linkedin'):
                  config.add_section('linkedin')
            config.set('linkedin', 'username', uname)
            config.set('linkedin', 'password', passwd)
            with open('config.ini', 'w') as configfile:
                  config.write(configfile)
      return uname, passwd

# Load LinkedIn cookies from config file
def load_cookies():
      config = configparser.ConfigParser()
      config.read('config.ini')
      try:
            li_at = config.get('linkedin', 'li_at')
            jsessionid = config.get('linkedin', 'JSESSIONID')
      except (configparser.NoSectionError, configparser.NoOptionError):
            print("LinkedIn cookies not found in config file.")
            li_at = input("Please enter your li_at cookie: ")
            jsessionid = input("Please enter your JSESSIONID cookie: ")
            if not config.has_section('linkedin'):
                  config.add_section('linkedin')
            config.set('linkedin', 'li_at', li_at)
            config.set('linkedin', 'JSESSIONID', jsessionid)
            with open('config.ini', 'w') as configfile:
                  config.write(configfile)
      return li_at, jsessionid

# Function to format the LinkedIn profile data
def profile_readable(parsed_data, post_data):
      # Extracting the name
      first_name = parsed_data['first_name']
      last_name = parsed_data['last_name']
      name = f"{first_name} {last_name}"

      # Formatting education details
      education_list = parsed_data['education']
      education_text = "Education:\n"
      for edu in education_list:
            school = edu.get('school_name', 'Unknown School')
            degree = edu.get('degree_name', 'Unknown Degree')
            field = edu.get('field_of_study', 'Unknown Field of Study')
            start_date = edu.get('start_date', {})
            end_date = edu.get('end_date', {})
            start_date_str = f"{start_date.get('month', '')}/{start_date.get('year', '')}" if start_date else "N/A"
            end_date_str = f"{end_date.get('month', '')}/{end_date.get('year', '')}" if end_date else "N/A"
            education_text += f"- {degree} in {field} from {school} (Start: {start_date_str}, End: {end_date_str})\n"

      # Formatting employment details
      employment_list = parsed_data['employment']
      employment_text = "Employment:\n"
      for job in employment_list:
            company = job.get('company_name', 'Unknown Company')
            title = job.get('title', 'Unknown Title')
            location = job.get('location', 'Unknown Location')
            description = job.get('description', 'No Description')
            start_date = job.get('start_date', {})
            end_date = job.get('end_date', {})
            start_date_str = f"{start_date.get('month', '')}/{start_date.get('year', '')}" if start_date else "N/A"
            end_date_str = f"{end_date.get('month', '')}/{end_date.get('year', '')}" if end_date else "N/A"
            employment_text += f"- {title} at {company}, {location} (Start: {start_date_str}, End: {end_date_str})\n  Description: {description}\n"

      # Formatting location
      location = parsed_data['location']
      location_text = f"Location: {location}\n"

      # Formatting industry
      industry = parsed_data['industry']
      industry_text = f"Industry: {industry}\n"

      # Formatting certifications
      certifications = parsed_data['certifications']
      certifications_text = "Certifications:\n"
      for cert in certifications:
            certName = cert.get('name', 'Unknown Certification')
            authority = cert.get('authority', 'Unknown Authority')
            start_date = cert.get('start_date', {})
            end_date = cert.get('end_date', {})
            start_date_str = f"{start_date.get('month', '')}/{start_date.get('year', '')}" if start_date else "N/A"
            end_date_str = f"{end_date.get('month', '')}/{end_date.get('year', '')}" if end_date else "N/A"
            certifications_text += f"- {certName} by {authority}, Start: {start_date_str}, End: {end_date_str})\n"

      posts = post_data
      posts_text = "Posts by the user:\n"
      for i, content in enumerate(posts, 1):
            posts_text += f"Post {i}: \n{content}\n----------------\n"

      return f"Name: {name}\n{location_text}\n{industry_text}\n{education_text}\n{employment_text}\n{certifications_text}", posts_text

# Function to parse the LinkedIn profile data
def parse_profile(profile_data):
      first_name = profile_data.get('firstName', '')
      last_name = profile_data.get('lastName', '')

      # Extract education details
      education = []
      for edu in profile_data.get('education', []):
            school_name = edu.get('schoolName', '')
            degree_name = edu.get('degreeName', '')
            field_of_study = edu.get('fieldOfStudy', '')
            start_date = edu.get('timePeriod', {}).get('startDate', {})
            end_date = edu.get('timePeriod', {}).get('endDate', {})
            education.append({
                  'school_name': school_name,
                  'degree_name': degree_name,
                  'field_of_study': field_of_study,
                  'start_date': start_date,
                  'end_date': end_date
            })

      # Extract employment details
      employment = []
      for exp in profile_data.get('experience', []):
            company_name = exp.get('companyName', '')
            title = exp.get('title', '')
            location = exp.get('locationName', '')
            description = exp.get('description', '')
            start_date = exp.get('timePeriod', {}).get('startDate', {})
            end_date = exp.get('timePeriod', {}).get('endDate', {})
            employment.append({
                  'company_name': company_name,
                  'title': title,
                  'location': location,
                  'description': description,
                  'start_date': start_date,
                  'end_date': end_date
            })

      # Extract location
      location = profile_data.get('locationName', '')

      # Extract industry
      industry = profile_data.get('industryName', '')

      # Extract certifications
      certifications = []
      for cert in profile_data.get('certifications', []):
            name = cert.get('name', '')
            authority = cert.get('authority', '')
            start_date = cert.get('timePeriod', {}).get('startDate', {})
            end_date = cert.get('timePeriod', {}).get('endDate', {})
            certifications.append({
                  'name': name,
                  'authority': authority,
                  'start_date': start_date,
                  'end_date': end_date
            })

      return {
            'first_name': first_name,
            'last_name': last_name,
            'education': education,
            'employment': employment,
            'location': location,
            'industry': industry,
            'certifications': certifications
      }

def extract_post_content(scraped_data):
    post_contents = []

    # Iterate through each post in the scraped data
    for actor in scraped_data:
        # Navigate to the content of the post
        commentary = actor.get('commentary', {})
        text_wrap = commentary.get('text', '')
        text = text_wrap.get('text', '')

        # Add the text content to the list if it exists
        if text:
            post_contents.append(text)

    return post_contents


def get_user(link):
      #uname, passwd = load_login_info()
      cookiejar = requests.cookies.RequestsCookieJar()
      li_at, jsessionid = load_cookies()
      cookiejar.set('li_at', li_at, domain='.linkedin.com', path='/')
      cookiejar.set('JSESSIONID', jsessionid, domain='.linkedin.com', path='/')
      api = Linkedin('', '', cookies=cookiejar)
      profile = api.get_profile(link)
      posts = api.get_profile_posts(link, None, 5)
      return profile_readable(parse_profile(profile), extract_post_content(posts))

#https://github.com/tomquirk/linkedin-api