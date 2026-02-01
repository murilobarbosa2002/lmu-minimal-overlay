# Configuration Guide

## Overview

The LMU Telemetry Overlay is **100% configurable** via JSON files. Every visual parameter, color, dimension, and behavior can be customized without touching any code.

## Configuration Files

### `config.json` - Main Configuration

Located in the project root, this file controls all visual and behavioral aspects of the overlay.

#### Complete Schema

```json
{
  "version": "1.0.0",
  "update_interval_ms": 16,
  
  "window": {
    "title": "LMU Telemetry Overlay",
    "default_width": 1920,
    "default_height": 1080
  },
  
  "theme": {
    "dashboard_card": {
      "bg_color": [10, 20, 30, 242],
      "bg_color_dragging": [25, 35, 50, 180],
      "text_color": [255, 255, 255],
      "gear_color": [255, 200, 0],
      "border_radius": 24,
      "border_color": [255, 255, 255, 30],
      "mask_color": [255, 255, 255],
      "lateral_padding": 20,
      "width": 350,
      "height": 130
    },
    
    "steering_indicator": {
      "radius": 45,
      "color_rim": [30, 30, 30],
      "color_marker": [255, 200, 0],
      "color_center": [50, 50, 50],
      "tick_start": 30,
      "tick_end": 150,
      "tick_step": 10
    },
    
    "bar": {
      "width": 18,
      "height": 70,
      "bg_color": [40, 40, 40],
      "border_radius": 3,
      "centerline_color": [100, 100, 100],
      "padding": 5,
      "font_size_value": 16,
      "font_size_label": 14
    },
    
    "indicator_bars": {
      "spacing": 12,
      "throttle_color": [0, 255, 0],
      "brake_color": [255, 0, 0],
      "ffb_color": [255, 165, 0]
    },
    
    "edit_mode": {
      "selection_color": [0, 255, 255],
      "selection_border_width": 2,
      "selection_border_radius": 8,
      "padding_min": 8,
      "padding_max": 12
    }
  },
  
  "defaults": {
    "telemetry": {
      "speed": 0.0,
      "rpm": 0,
      "max_rpm": 8000,
      "gear": 0,
      "throttle_pct": 0.0,
      "brake_pct": 0.0,
      "clutch_pct": 0.0,
      "steering_angle": 0.0,
      "ffb_level": 0.0,
      "unit": "km/h"
    }
  },
  
  "colors": {
    "ffb_normal": [0, 255, 0],
    "ffb_warning": [255, 255, 0],
    "ffb_clipping": [255, 0, 0]
  },
  
  "thresholds": {
    "ffb_warning": 0.8,
    "ffb_clipping": 0.95
  },
  
  "performance": {
    "fps_target": 60
  }
}
```

---

## Configuration Sections

### Window Configuration

Controls window properties:

```json
"window": {
  "title": "LMU Telemetry Overlay",
  "default_width": 1920,
  "default_height": 1080
}
```

- **title**: Window title bar text
- **default_width**: Initial window width in pixels
- **default_height**: Initial window height in pixels

---

### Theme Configuration

#### Dashboard Card

Main widget appearance:

```json
"dashboard_card": {
  "bg_color": [10, 20, 30, 242],           // RGBA background
  "bg_color_dragging": [25, 35, 50, 180],  // RGBA when dragging
  "text_color": [255, 255, 255],           // RGB text color
  "gear_color": [255, 200, 0],             // RGB gear indicator
  "border_radius": 24,                      // Corner roundness
  "border_color": [255, 255, 255, 30],     // RGBA border
  "mask_color": [255, 255, 255],           // RGB mask
  "lateral_padding": 20,                    // Internal padding
  "width": 350,                             // Widget width
  "height": 130                             // Widget height
}
```

#### Steering Indicator

Steering wheel visualization:

```json
"steering_indicator": {
  "radius": 45,                    // Wheel radius in pixels
  "color_rim": [30, 30, 30],      // RGB rim color
  "color_marker": [255, 200, 0],  // RGB marker color
  "color_center": [50, 50, 50],   // RGB center dot color
  "tick_start": 30,                // Tick marks start angle
  "tick_end": 150,                 // Tick marks end angle
  "tick_step": 10                  // Tick marks step
}
```

#### Bar (Pedal Indicators)

Individual bar appearance:

```json
"bar": {
  "width": 18,                        // Bar width in pixels
  "height": 70,                       // Bar height in pixels
  "bg_color": [40, 40, 40],          // RGB background
  "border_radius": 3,                 // Corner roundness
  "centerline_color": [100, 100, 100], // RGB centerline (FFB)
  "padding": 5,                       // Internal padding
  "font_size_value": 16,             // Percentage font size
  "font_size_label": 14              // Label font size
}
```

#### Indicator Bars

Bar layout and colors:

```json
"indicator_bars": {
  "spacing": 12,                   // Space between bars
  "throttle_color": [0, 255, 0],  // RGB throttle
  "brake_color": [255, 0, 0],     // RGB brake
  "ffb_color": [255, 165, 0]      // RGB FFB
}
```

#### Edit Mode

Selection visual feedback:

```json
"edit_mode": {
  "selection_color": [0, 255, 255],  // RGB selection border
  "selection_border_width": 2,        // Border thickness
  "selection_border_radius": 8,       // Corner roundness
  "padding_min": 8,                   // Min breathing padding
  "padding_max": 12                   // Max breathing padding
}
```

---

## Creating Custom Themes

### Example: Dark Theme

```json
{
  "theme": {
    "dashboard_card": {
      "bg_color": [5, 5, 5, 250],
      "text_color": [200, 200, 200],
      "gear_color": [100, 200, 255]
    },
    "indicator_bars": {
      "throttle_color": [50, 200, 50],
      "brake_color": [200, 50, 50],
      "ffb_color": [200, 150, 50]
    }
  }
}
```

### Example: High Contrast Theme

```json
{
  "theme": {
    "dashboard_card": {
      "bg_color": [0, 0, 0, 255],
      "text_color": [255, 255, 255],
      "gear_color": [255, 255, 0]
    },
    "steering_indicator": {
      "color_marker": [255, 0, 255]
    },
    "indicator_bars": {
      "throttle_color": [0, 255, 0],
      "brake_color": [255, 0, 0],
      "ffb_color": [255, 255, 0]
    }
  }
}
```

---

## Color Format

All colors use RGB or RGBA format:

- **RGB**: `[Red, Green, Blue]` - Values 0-255
- **RGBA**: `[Red, Green, Blue, Alpha]` - Values 0-255, Alpha controls transparency

**Examples:**
- Pure Red: `[255, 0, 0]`
- Semi-transparent Blue: `[0, 0, 255, 128]`
- White: `[255, 255, 255]`
- Black: `[0, 0, 0]`

---

## Best Practices

1. **Backup**: Always backup `config.json` before making changes
2. **Validation**: Invalid JSON will cause the app to use defaults
3. **Colors**: Use RGBA for backgrounds to control transparency
4. **Testing**: Test changes in development mode first
5. **Themes**: Create separate theme files and copy sections as needed

---

## Troubleshooting

### Config Not Loading
- Check JSON syntax (use a validator)
- Ensure file is named `config.json` exactly
- Check file permissions

### Colors Look Wrong
- Verify RGB values are 0-255
- Check alpha channel for transparency
- Ensure proper array format `[R, G, B]` or `[R, G, B, A]`

### Layout Issues
- Check dimension values (width, height, padding)
- Verify spacing and radius values are positive integers
- Ensure values are appropriate for your screen resolution

---

## See Also

- [API Reference: ConfigManager](../api-reference/configuration/config-manager.md)
- [User Guide: Customization](customization.md)
- [Quick Start](quick-start.md)
