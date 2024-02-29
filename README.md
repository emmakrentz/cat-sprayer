# Automated Cat Spray Bottle
My sweet cat has one (1) rule he is required to follow in the whole world-- he is not permitted on the kitchen counter. Of course this means that it is his solitary mission in life to get on the counter whenever possible. In the day I will manually spray him, but at night I turn off the lights and hear his evil little paws hopping up on the marble and there's nothing I can do.

Until now! I built an automatic cat sprayer that sprays him when he jumps on the counters. But I use the counters, and don't want to get sprayed each time I am unloading groceries or cooking dinner or building cat-spray robots. So this robot uses image recognition code trained on the Coco objects files from OpenCV (code mostly from https://core-electronics.com.au/guides/object-identify-raspberry-pi/#Set) to detect my cat. 

First, an ultrasonic sensor is constantly sending distance readings to the RPi. If this distance drops below the distance to the far wall (i.e. something has blocked its path), it triggers the image rec code to run. If a cat is detected, a servo motor presses against the trigger of an electronic spray bottle. Otherwise if no cat is found in 10 seconds, it times out, and goes back to only distance sensing. 

This works remarkably well. Sorry Pumpkin.
