
import time
import sys

from webgoose import PageQuerier
from webgoose import Renderer
from webgoose import SiteQuerier
from webgoose.structs import PageInfo


class BuildHandler:

    def __init__(self):

        """
        
        """

        self.build_report = dict()
        self.__build_time = time.time()
        self.__site_info = None



    @property
    def build_time(self) -> float:
        return self.__build_time



    @property
    def site_info(self):
        return self.__site_info



    def pre_flight_checks(self) -> bool:

        """
        Responsible for Checking Whether Site Can Be Built

        Checks, Source & Build Dir Accessbility, Config Correctness, etc
        """

        return True



    def configure(self) -> None:

        """

        """

        if self.pre_flight_checks():

            # Initialise Site Querier Instance
            querier = SiteQuerier(self.build_time)

            # Set SiteInfo Object Retrieved For Querier
            self.site = querier.get_site_info()

        else:

            print("Failed To Configure Build Handler")
            sys.exit()



    def build_all(self):

        """

        """

        # Pages For Build Identified By SiteQuerier
        to_build = self.site.pages

        for page_obj in to_build:

            try:

                # Query Contents Of Page
                page = PageQuerier(page_obj).get_page_info()

                # Build The Page
                final_page = self.build_page(page)

                # Output The Page To File
                print(final_page)
                pass

                # Update Build Report
                self.build_report[page_obj.path] = True

            except Exception as e:
                
                # Print Error To User
                print(f"Error Building Page '{page_obj.path}':\nException: {str(e)}")

                # Update Build Report
                self.build_report[page_obj.path] = False

                # Skip This Page
                continue


        # Output Build Report and Exit
        self.output_build_report()
    


    def build_page(self, page: PageInfo) -> bool:

        """

        """

        # Initialise Page Renderer Instance With PageInfo Object
        renderer = Renderer(page)

        # Arguments Dict For Jinja2 Templating
        args = {'site': self.site, 'page': page}

        # Render Page and Return
        # (MAY THROW EXCEPTION)
        return renderer.render(args)



    def output_build_report(self):

        """

        """

        # Seperate Failed and Successful Builds
        success = {path:status for path, status in self.build_report.items() if status == True}
        fail = {path:status for path, status in self.build_report.items() if status == False}

        # Print Seperator and Header
        print("-------\nBuild Report:")

        # Print Successfully Built Pages
        for path in success.keys():
            print(f"SUCCESS: '{path}'")
        
        # Print Failed Pages
        for path in fail.keys():
            print(f"!! FAILED: '{path}'")

        # Print Num of Success & Fail
        print(f"\n{len(fail)} Failures, {len(success)} Pages Built")

        # Print Seperator
        print("-------")