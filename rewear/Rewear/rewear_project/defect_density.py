import subprocess
import re

lines = 800
bugs = 7

def calculate_defect_density(project_path):
    try:
        # Run cloc command to count lines of code
        output = subprocess.check_output(['cloc', project_path, '--csv']).decode('utf-8')

        # Extract relevant information from the output
        lines_of_code = 0
        comments = 0
        blanks = 0

        for line in output.split('\n'):
            if line.startswith('SUM:'):
                values = re.findall(r'\d+', line)
                if len(values) >= 3:
                    lines_of_code = int(values[0])
                    comments = int(values[1])
                    blanks = int(values[2])
                break

        # Calculate defect density
        total_lines = lines_of_code + comments + blanks
        defect_density = (lines_of_code + comments) / total_lines if total_lines != 0 else 0

        return defect_density

    except subprocess.CalledProcessError:
        print('Error: Failed to run cloc command.')
        return None


# Usage example

project_path = '/rewear/Rewear/rewear_project'
# defect_density = calculate_defect_density(project_path)

defect_density = bugs/lines


if defect_density is not None:
    print(f'Defect Density: {defect_density:.2%}')
