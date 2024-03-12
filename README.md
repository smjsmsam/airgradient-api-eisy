
# Example 1 Node Server (c) 2021 Robert Paauwe

A simple node server that demonstrates how to create a node server that
doesn't have a controller node and only creates device nodes.  This node
server simply increments a counter and updates GV0 and GV1 with the updated
count at every poll() interval.

## Installation


### Node Settings
The settings for this node are:

#### Short Poll
   * How often to increment the count
#### Long Poll
   * Not used

#### multiplier
   * Apply the multiplier to count and save in GV1


## Requirements

1. Polyglot V3.
2. ISY firmware 5.3.x or later

# Release Notes

- 1.0.0 08/11/2021
   - Initial version published to github
