import requests
import configparser
from linkedin_api import Linkedin
import sys
import json

from SocialService.SocialService import SocialService
from const import Const
from AIService.AIRender import AIRender

class LinkedinService(SocialService):
    def __init__(self) -> None:
        super().__init__()

    async def single_user_cli(self, username: str, output: str, payload: str, ai: str, template: str, api_key: str = ""):
        profile, posts = self._get_user(username)
        if profile == None:
            print(f"{Const.COLOR_ERROR}User not found{Const.RESET_ALL}")
            return
        
        Ai = AIRender(ai).model

        print(Ai.generate_prompt_linkedin(profile, posts, output, payload, ai, template, api_key=api_key))
        sys.exit()

    async def user_list_cli(self, file_path: str, output: str, payload: str, ai: str, template: str, api_key: str = ""):
        try:
            with open(file_path, 'r') as file:
                usernames = file.readlines()
        except:
            print(f"{Const.COLOR_ERROR}File not found{Const.RESET_ALL}")
            return
        clean_usernames = []
        for user in usernames:
            if '\n' in user:
                user = user[:-1]
            clean_usernames.append(user)
        profile_list = []
        posts_list = []
        for user_id in clean_usernames:
            profile, posts = self._get_user(user_id)
            if profile == None:
                print(f"{Const.COLOR_ERROR}User {user_id} not found{Const.RESET_ALL}")
                profile_list.append(None)
                posts_list.append(None)
                continue
            profile_list.append(profile)
            posts_list.append(posts)
        generation_option = self._linkedin_generation_options()
        payload = self._payload_options()
        template = self._template_options()

        Ai = AIRender(ai).model

        for profile, posts in zip(profile_list, posts_list):
            print(f"{user['username']}:")
            print(Ai.generate_prompt_linkedin(profile, posts, generation_option, payload, ai, template, api_key=api_key))

    async def single_user(self, ai: str):
        print("\n\nPlease enter the user ID of the user you would like to scrape:")
        print("(the user ID is in the URL of the user's profile like this: https://www.linkedin.com/in/user-id/)")
        user_id = input("\nUser ID: ")
        profile, posts = self._get_user(user_id)
        if profile == None:
            print(f"{Const.COLOR_ERROR}User not found{Const.RESET_ALL}")
            return self.single_user()
        generation_option = self._linkedin_generation_options()
        payload, payload_text = self._payload_options()
        template = self._template_options()

        Ai = AIRender(ai).model

        print(Ai.generate_prompt_linkedin(profile, posts, generation_option, payload, ai, template, payload_text, api_key=""))

    async def user_list(self, ai: str):
        print("\n\nPlease enter the path to the file containing the list of usernames you would like to scrape:")
        file_path = input("\nFile path: ")
        try:
                with open(file_path, 'r') as file:
                    usernames = file.readlines()
        except:
                print(f"{Const.COLOR_ERROR}File not found{Const.RESET_ALL}")
                return self.user_list(ai)
        clean_usernames = []
        for user in usernames:
                if '\n' in user:
                    user = user[:-1]
                clean_usernames.append(user)
        profile_list = []
        posts_list = []
        for user_id in clean_usernames:
                profile, posts = self._get_user(user_id)
                if profile == None:
                    print(f"{Const.COLOR_ERROR}User {user_id} not found{Const.RESET_ALL}")
                    profile_list.append(None)
                    posts_list.append(None)
                    continue
                profile_list.append(profile)
                posts_list.append(posts)
        generation_option = self._linkedin_generation_options()
        payload = self._payload_options()
        template = self._template_options()

        Ai = AIRender(ai).model

        for profile, posts in zip(profile_list, posts_list):
            print(f"{user['username']}:")
            print(Ai.generate_prompt_linkedin(profile, posts, generation_option, payload, ai, template, api_key=""))

    # ! --------------------------------------------------------------------------------
    # ! PRIVATE
    # ! --------------------------------------------------------------------------------

    def _get_user(self, link):
        cookiejar = requests.cookies.RequestsCookieJar()
        li_at, jsessionid = self._load_cookies()
        cookiejar.set('li_at', li_at, domain='.linkedin.com', path='/')
        cookiejar.set('JSESSIONID', jsessionid, domain='.linkedin.com', path='/')
        api = Linkedin('', '', cookies=cookiejar)
        profile = api.get_profile(link)
        posts = api.get_profile_posts(link, None, 5)
        return self._profile_readable(self._parse_profile(profile), self._extract_post_content(posts))
    
    def _load_cookies(self):
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
    
    def _profile_readable(self, parsed_data, post_data):
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

    def _parse_profile(self, profile_data):

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
    
    def _extract_post_content(self, scraped_data):
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
    
    def _linkedin_generation_options(self):
        generation_option = 0
        print("\n\nPlease select what to generate:")
        self._print_options(Const.generation_options_list_linkedin)
        generation_option = self._get_valid_input(len(Const.generation_options_list_twitter))
        return generation_option

    def _payload_options(self):
        payload_option_text = ""
        print("\n\nPlease select a type of payload:")
        self._print_options(Const.payload_options_list)
        payload_option = self._get_valid_input(len(Const.payload_options_list))
        if payload_option == 4:
            payload_option_text = input("\Please specify the type of payload: ")
        return payload_option, payload_option_text
    
    def _template_options(self):
        template_option = input("\n\nDo you want to use a template? (y/n) ")
        if template_option == "n":
            return False
        elif template_option != "y":
            print(f"{Const.COLOR_ERROR}Invalid option{Const.RESET_ALL}")
            return self._template_options()
        print("\n\nPlease write the template name or enter '?' to see the list of available templates:")
        with open ('templates.json', 'r') as file:
            templates = json.load(file)
        template_names = list(templates.keys())
        while True:
            template_name = input("\nTemplate name: ")
            if template_name == "?":
                print("\n\nAvailable templates:")
                self._print_options(template_names)
            elif template_name not in template_names:
                print(f"{Const.COLOR_ERROR}Invalid template name{Const.RESET_ALL}")
            else:
                return templates[template_name]

