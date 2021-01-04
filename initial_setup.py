from printer.models import Settings

x = Settings(
    id=1,
    app_title='GUI Print Server',
    default_color='RGB',
    default_orientation='3',
    printer_profile='None found'
)
x.save()