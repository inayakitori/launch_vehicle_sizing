# Launch Vehicle Sizing
## Goal
To be able to find the minimum cost for a single-use rocket that will deliver a satellite into orbit. To then create a report for said single use rocket sizing
One big assumption that will be made is that a lighter rocket is always cheaper, and so a proxy goal will be to minimise the overall launch mass.

## Problem description
Variables:
- The payload size and final altitude
- The exhaust velocities and structural mass fractions of different possible launch vehicles and space propulsion srms 
- The number of stages

What to find:
- The different stages used
- The mass of each stage

## Proposed approach
Modelling the problem as a minimisation problem for a set number of stages. Finding what launch vehicles and SRMS would work best with a set number of stages. create a function:

  payload_fraction(stages_used, proportion_dv_each_stage)
  
where:

  stages_used: array of (v_exhaust, structural_mass_fraction)
  
  proportion_dv_each_stage: array of floats from 0 to 1
  
the sum of proportions will be 1.

and then find the values of proportion_dv_each_stage that minimise payload_fraction

## Completion timeline
Mon 7th Oct setup + payload_fraction function
Wed 9th Oct input parsing
Fri 11th Oct minimisation via scipy
Sun 13th Oct readable and usable output
Fri 18th Oct report writing
Mon 21st Oct deadline
Mon 21st Oct reflection/celebration (in here)

## Reflection
This is where overall challenges and general stuff will be logged.

## References
engine database: https://planet4589.org/space/gcat/web/lvs/engines/index.html