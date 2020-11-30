# ROS

```bash
# Catkin aliases
alias cknm="catkin_make"
alias cknmpy3="cknm -DPYTHON_EXECUTABLE=/usr/bin/python3"
alias cknpc="catkin_create_pkg"

# ROS aliases
# run this when in your workspace
# rosiws (ROS initialize workspace) is enough to just set everything up
alias rossrc="source devel/setup.sh"
alias rospath='echo "$ROS_PACKAGE_PATH"'
alias rosiws="rossrc && rospath"
```
