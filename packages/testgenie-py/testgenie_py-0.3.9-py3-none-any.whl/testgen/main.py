from testgen.service.service import Service
from testgen.controller.cli_controller import CLIController
from testgen.generator.unit_test_generator import UnitTestGenerator

def main():
    service = Service()
    controller = CLIController(service)
    controller.run()

if __name__ == '__main__':
    main()