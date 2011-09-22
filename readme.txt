

Image Gallery is an application to view images stored on the local computer.

This application does not work like the other application of the sort, 
instead it mimics the look and feel of an website.

It is built with PyQt4 and webkit.

The root folder of images must be specified in config.xml.

This application is not very flexible because it expects a certain structure of
the folders used to store the images.

    Example:
        - root folder
            - Gallery Animals
                - Zebra
                    1.jpg
                    2.jpg
                    3.jpg
                    ...
                ...
            ...
            - Gallery Cars
                - Aston Martin
                    - 1.jpg
                    - 2.jpg
                    - 3.jpg
                    ...
                ...
            ...