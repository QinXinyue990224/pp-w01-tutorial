# Module to create widgets revealing exercise solutions.
# Example use in a notebook:
#
# import show_solutions
# show_solutions.show('week01_ex1')
#
# Shows an accordion menu to reveal/hide solutions tagged with 'week01_ex1'
# in the solutions script 'week01_solutions.txt'.

# Import display functions
import ipywidgets as widgets
from IPython.display import display, Code, Markdown

def show(question):
    '''
    Displays solution to a particular question.
    
    Input:
    question (str): string of the form 'weekXX_exY'
    '''

    week = question.split('_')[0]

    # Create output area for the solution
    sol_area = widgets.Output(layout={'border': '1px solid green'})

    # Create accordion
    acc = widgets.Accordion(children=[sol_area], selected_index=None)
    acc.set_title(0, 'Solution')

    # Read solutions from file
    try:
        # Retrieve solution code from script, as a string
        with open(f'{week}_solutions.txt', 'r') as f:
            sol = []
            sol_block = ''
            out_format = []
            write_line = False

            # Read line-by-line
            for l in f:
                if l.startswith(f'###{question}_start'):
                    # Found starting tag, get format
                    out_format.append(l.strip().split('_')[-1])

                    # Start writing at the next line
                    write_line = True
                    continue

                # Continue writing lines until end tag
                if write_line:
                    if l.startswith(f'###{question}_end'):
                        # Reached the end tag, stop reading file
                        write_line = False
                        sol.append(sol_block)
                        break
                    elif l.startswith(f'###{question}_switch'):
                        # Switching output format for the next lines
                        out_format.append(l.strip().split('_')[-1])
                        sol.append(sol_block)
                        sol_block = ''
                        continue
                    else:
                        # Write line to current block
                        sol_block += l

    except FileNotFoundError:
        sol = 'Solutions not yet released!'
        out_format = {}

    # Display solutions
    if not out_format:
        # Not yet released
        print(sol)
    else:
        # Display block by block
        for sol_block, fmt in zip(sol, out_format):
            if fmt == 'py':
                sol_area.append_display_data(Code(data=sol_block, language='py'))
            elif fmt == 'md':
                sol_area.append_display_data(Markdown(data=sol_block))
            else:
                sol_area.append_stdout(print('Format not recognised...'))

        # Display the accordion
        display(acc)
