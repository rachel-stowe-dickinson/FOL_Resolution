This is a tool for verifying resolution proofs in first order logic.

The tool uses a simple Python user interface to complete the steps of a resolution proof. The program first collects FOL formulae from the user that 
are in CNF and prenex normal form. The user can then skolemize any formulae that contain quantifiers. Finally, the proof can be conducted through a 
series of resolution and/or unification steps until the user is satisfied with the result. The proof's output will be saved to a JSON file.

Run the file fo_parser.py to begin using the tool.

This project was was a collaborative effort by Rachel Dickinson and Aarthy Kesavan Padmanaban. Inspiration for the resolution portion of the project 
was taken from the following repository by Adithya Murali: https://github.com/muraliadithya/logictools.
