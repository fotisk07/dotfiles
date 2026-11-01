-- See https://wiki.hypr.land/Configuring/Basics/Monitors/
-- List current monitors and supported resolutions with: hyprctl monitors all

local omarchy_gdk_scale = 1
local omarchy_monitor_scale = 1.25

hl.env("GDK_SCALE", tostring(omarchy_gdk_scale))
hl.monitor({ output = "", mode = "preferred", position = "auto", scale = omarchy_monitor_scale })

-- External monitor on the left; laptop display on the right.
-- At 1.6 scale, the external monitor is 1200 logical pixels wide.
hl.monitor({ output = "DP-2", mode = "1920x1080@60", position = "0x0", scale = 1.6 })
hl.monitor({ output = "eDP-1", mode = "1920x1200@59.95", position = "1200x0", scale = 1.25 })

-- Portrait/rotated secondary monitor (transform: 1 = 90°, 3 = 270°).
-- hl.monitor({ output = "DP-4", mode = "preferred", position = "auto", scale = 1, transform = 1 })
