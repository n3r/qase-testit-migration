from .support import ConfigManager, Logger, Mappings, ThrottledThreadPoolExecutor, Pools
from .service import QaseService, TestItService
from .entities import Fields, Projects, Suites, Cases, Attachments
from concurrent.futures import ThreadPoolExecutor


class TestItImporter:
    def __init__(self, config: ConfigManager, logger: Logger) -> None:
        self.pools = Pools(
            qase_pool=ThrottledThreadPoolExecutor(max_workers=8, requests=230, interval=10),
            tr_pool=ThreadPoolExecutor(max_workers=8),
        )

        self.logger = logger
        self.config = config

        self.qase_service = QaseService(config, logger)
        self.testit_service = TestItService(config, logger)

        self.active_project_code = None

        self.mappings = Mappings(self.config.get('users.default'))

    def start(self):
        # Step 1. Import project and build projects map
        self.mappings = Projects(
            self.qase_service, 
            self.testit_service, 
            self.logger, 
            self.mappings,
            self.config,
            self.pools,
        ).import_projects()

        # Step 4. Import custom fields
        #self.mappings = Fields(
        #    self.qase_service, 
        #    self.testit_service, 
        #    self.logger, 
        #    self.mappings,
        #    self.config,
        #    self.pools,
        #).import_fields()

        # Step 5. Import projects data in parallel
        with ThreadPoolExecutor(max_workers=8) as executor:
            futures = []
            for project in self.mappings.projects:
                # Submit each project import to the thread pool
                future = executor.submit(self.import_project_data, project)
                futures.append(future)

            # Wait for all futures to complete
            for future in futures:
                # This will also re-raise any exceptions caught during execution of the callable
                future.result()

        self.mappings.stats.print()

    def import_project_data(self, project):
        self.logger.print_group(f'Importing project: {project["name"]}')

        self.mappings = Suites(
            self.qase_service,
            self.testit_service,
            self.logger,
            self.mappings,
            self.config,
            self.pools,
        ).import_suites(project)

        Cases(
            self.qase_service,
            self.testit_service,
            self.logger,
            self.mappings,
            self.config,
            self.pools,
        ).import_cases(project)
