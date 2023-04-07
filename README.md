# shortestRouteDeviation
GoogleMaps only provides the shortest path from Point A to Point B. It's common to want to travel from Point A to Point B on a long trip and make a stop at a franchise, such as McDonald's. In this case, we don't care which franchise we stop at, we just want to choose the franchise that deviates the least possible from our main trip.

For this project, we use OpenRouteService's time and distance estimation to compute the franchise that deviates the least from our main trip in terms of time and distance.

## Configuration
`pip install -r requirements.txt`

Replace API\_KEY with your API key in "main.py".

You can generate a KEY here: https://openrouteservice.org/
## How to use

Execute the following command:

```$ python main.py ```

And reply to the 3 questions asked with your own details. Hereafter an example is presented.

```
Introduce the destination
>Dublin 1
Introduce the origin
>Dublin 2
Introduce the franchise name
>McDonald's



In terms of distance, the best franchise is: 53.3454829 -6.2635981
Estimated total travel time: 628.50. seconds
Estimated total travel distance: 3645.00. meters
------------------------------------------------------------
In terms of time, the best franchise is: 53.3509526 -6.2644416
Estimated total travel time: 573.40. seconds
Estimated total travel distance: 3832.90. meters
```
