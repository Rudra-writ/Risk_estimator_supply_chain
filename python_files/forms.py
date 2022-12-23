from django import forms


CHOICES = (

("Pressure", "Pressure"),
("Filter Status", "Filter Status"),
("Gas flow speed", "Gas flow speed"),
("Gas pump power", "Gas pump power"),
("Oxygen top", "Oxygen top"),
("Oxygen bottom", "Oxygen bottom"),
("Oxygen 1 ppm", "Oxygen 1 ppm"),
("Oxygen 2 ppm", "Oxygen 2 ppm"),
("Dew point dryer", "Dew point dryer"),
("Dew point process gas", "Dew point process gas"),
("Gas Temp", "Gas Temp"),
("Platform", "Platform"),
("Build Chamber", "Build Chamber"),
("Optical Bench", "Optical Bench"),
("Collimator", "Collimator"),
("Compressed air inlet pressure", "Compressed air inlet pressure"),
("Inert gas inlet pressure", "Inert gas inlet pressure"),
("Pump", "Pump"),
("Cabinet", "Cabinet"),
("Cabinet 2", "Cabinet 2"),
("Ambiance", "Ambiance"),
("MemTotal", "MemTotal"),
("MemProcess", "MemProcess"),
("Laser Emission Flags", "Laser Emission Flags"),
("Laser On Flags", "Laser On Flags"),
("Galvo X0", "Galvo X0"),
("Galvo Y0", "Galvo Y0"),
("Servo X0", "Servo X0"),
("Servo Y0", "Servo Y0"),
("Galvo X1", "Galvo X1"),
("Galvo Y1", "Galvo Y1"),
("Servo X1", "Servo X1"),
("Servo Y1", "Servo Y1"),

)
        
class SensorsForm(forms.Form):
    
    filters = forms.MultipleChoiceField( choices=CHOICES, label= '')