# gopro-file-organizer

A program to rename the gopro files according to a more logical convention.


This small project combines several steps in a python development, which are
very interesting to learn and which can be tested directly here.

## Implementation plan - the roadmap


[ ] check the case if one or more files from a series are missing in both the 
    forward rename and the reverse rename procedure.

    
[x]  1. create initial function 'compile_filename' to implement the regular 
        expressions for the file identification
        
[x]  2. create manual list with 'generate_random_test_names' to check the 
        performance of the regular expression method 'compile_filename'
        
[x]  3. Implement method 'create_sorted_lists' which takes a filelist and sorts
        them in separete lists. These lists can then be processed further.
        
[x]  4. Implement testing methods 'gen_rnd_file_list', 'gen_rnd_chap_list' and
        'gen_rnd_burst_loop_list' to create automatically random file lists to
        benchmark and check the performance of the method 'create_sorted_lists'.
        
[x]  5. Implement a renaming procedure for each group of lists to output a 
        the current list together with the renamed items. This will be 
        essentially the dry run for the filename renamer.
        
[ ]  6. Implement the revers run, so that a new filename style will be 
        tranformed into the old one. This will ensure that one can establish 
        the previous state.
        
[ ]  7. Implement a similar function like 'create_sorted_lists' but now for the
        new file names to presort the files, which need to be renames back.
        
[x]  8. Implement methods, which generate a random lists for each scenario of 
        the new renaming scheme, so that it can be used for testing the reverse
        algorithm.
        
[ ]  9. Implement a new file for the unit-test, which makes use of the generate
        functions for random names and check whether the outcome works for 10000
        as expected.
        
[x] 10. Implement the actual renaming function, which gets the current name and
        the target name, and the renaming will happen here. 
        
[]  11. Implement a checking routines, whether the file exists or not. Moreover it will
        check whether file can be actually renamed or whether it is looked or
        read by another program.
        
[x] 12. Implement a method, which extracts all files from a folder

[ ] 13. Implement a method, which recursively extracts all files from all folder
        of a given path.
        
[ ] 14. Make a wrapper function, which can take multiple filepaths, and which 
        will run through each filepath and perform a single folder file 
        extraction, implemented in 9.
        
[ ] 15. Make a connection function, which connects the extracted file lists with
        the renaming procedure.
        
[ ] 16. Start to sort the create methods either in separate files, or make a 
        proper class structure to structure the code behavior.
        
[ ] 17. Implement a ui file for the renamer.

[ ] 18. Create a qt eventloop and let a test renaming procedure run within this
        eventloop. Close the loop after the renaming has been run.
        
[ ] 19. Integrate the gui in the event loop and make a rename button, which 
        executes a dry test.
        
[ ] 20. Create a gui file to connect the signals from the display units in the
        ui files. Moreover, the display units should pass its entries to the
        appropriate functions.
        
[ ] 21. Make the renaming function run in its own thread, so that it can be 
        stopped on request.
        
[ ] 22. Create a pypy project, which bundles the core renaming methods in a
        library which can be installed with pip.
        
[ ] 23. Create a conda environment or an dependency filelist, so that others can
        install and test the code.
        
[ ] 24. Bundle the GUI and the core modules to an executable file on windows.
        Describe the setup procedure. This denotes version 1.0.
        
[ ] 25. Bundle the GUI and the core modules to executable for linux(debian).

[ ] 26. Bundle the GUI and the core modules to executable for mac.

[ ] Implement continuous integration which utilizes the unit-test methods to 
    check the build process if new pushes occur on github.
        
