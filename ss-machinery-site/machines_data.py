"""Single source of truth for S&S machine content (pages + listing pack)."""

BUSINESS = dict(
    name='S&S Machinery', legal='Sayed and Sons Machinery Sales and Hire',
    phone='0466 892 400', phone_tel='+61466892400', email='sales@sandsmachinery.com.au',
    web='sandsmachinery.com.au', site='https://www.sandsmachinery.com.au',
    address='Factory 5, 65-67 Hallam South Road, Hallam VIC 3803',
    suburb='Hallam, VIC',
    warranty='5 year / 200 hour warranty', services='First 3 services free',
    delivery=[('Within 25 km of Hallam', '$120 each way'), ('25–50 km of Hallam', '$180 each way'), ('Pick up from our Hallam yard', 'Free')],
    delivery_note='Delivery prices ex GST. Longer distances quoted on request.',
    multi_bucket='Multi (4-in-1) bucket upgrade +$1,500 on any loader',
    attachments=['Standard bucket (included)', 'Multi / 4-in-1 bucket (+$1,500)', 'Auger drive & bits (price on request)', 'Stump grinder (price on request)'],
    hire_line='Hire by the day or week — rates and availability on request.',
)

MACHINES = [
    dict(
        key='HM370T', slug='hm-370t', name='HM 370T', colour='green',
        type='Stand-on tracked mini loader', cls='Mini loader',
        tagline='Compact tracked mini loader that fits through a standard gate.',
        price=14999, price_note='inc. GST, with standard bucket',
        engine='Briggs & Stratton 23 HP petrol',
        specs=[('Engine', 'Briggs & Stratton 23 HP petrol'), ('Operating weight', '1,176 kg'),
               ('Rated operating load', '350 kg'), ('Maximum lift capacity', '480 kg'),
               ('Undercarriage', 'Rubber tracks'), ('Operator position', 'Stand-on platform'),
               ('Standard attachment', 'General purpose bucket'), ('Optional', 'Multi bucket, auger, stump grinder')],
        blurb=('The HM 370T is the loader for tight access jobs: landscaping, fencing, post holes, '
               'backyard renovations and anything a wheelbarrow used to do. Stand-on tracked design, '
               'Briggs & Stratton 23 HP power and a 480 kg lift capacity in a machine that fits through a standard gate.'),
        bullets=['Fits through a standard gate', 'Rubber tracks — low ground pressure on lawns and pavers',
                 'Briggs & Stratton 23 HP petrol engine', '480 kg max lift / 350 kg rated operating load',
                 'Quick-hitch for buckets, auger and stump grinder'],
        uses=['Landscaping and turf prep', 'Fencing and post holes (with auger)', 'Backyard and tight-access earthworks', 'Hire fleets and owner-operators'],
        spin_n=6,
    ),
    dict(
        key='HM380T', slug='hm-380t', name='HM 380T', colour='red',
        type='Stand-on tracked mini loader', cls='Mini loader',
        tagline='Honda-powered mini loader, pictured with the auger attachment.',
        price=17999, price_note='inc. GST, with standard bucket (auger pictured — priced separately)',
        engine='Honda 17.5 kW petrol',
        specs=[('Engine', 'Honda 17.5 kW petrol'), ('Operating weight', '870 kg'),
               ('Bucket capacity', '0.12 m³'), ('Undercarriage', 'Rubber tracks'),
               ('Operator position', 'Stand-on platform (fold-down)'), ('Standard attachment', 'General purpose bucket'),
               ('Optional', 'Multi bucket, auger (pictured), stump grinder')],
        blurb=('The HM 380T pairs a Honda engine with a light 870 kg tracked chassis — easy to trailer, easy on '
               'lawns, and quick to swap between bucket, auger and stump grinder. Pictured with the auger drive '
               'fitted, the set-up fencing contractors ask for.'),
        bullets=['Honda 17.5 kW petrol engine', 'Only 870 kg — tows behind a ute on a standard trailer',
                 'Fold-down stand-on platform', 'Rubber tracks', 'Auger, multi bucket and stump grinder options'],
        uses=['Fencing and post holes', 'Garden and landscape construction', 'Tight access sites', 'Hire fleets'],
        spin_n=6,
    ),
    dict(
        key='HM750T', slug='hm-750t', name='HM 750T', colour='yellow',
        type='Stand-on tracked mini loader', cls='Mini loader',
        tagline='Kubota diesel mini loader with 580 kg lift.',
        price=24999, price_note='inc. GST, with standard bucket',
        engine='Kubota 25 HP diesel',
        specs=[('Engine', 'Kubota 25 HP diesel'), ('Operating weight', '1,400 kg'),
               ('Rated operating load', '400 kg'), ('Maximum lift capacity', '580 kg'),
               ('Undercarriage', 'Rubber tracks'), ('Operator position', 'Stand-on platform'),
               ('Standard attachment', 'General purpose bucket'), ('Optional', 'Multi bucket, auger, stump grinder')],
        blurb=('Step up to diesel. The HM 750T runs a Kubota 25 HP engine on a 1,400 kg tracked chassis, '
               'lifting 580 kg — the all-day machine for landscapers and builders who want diesel economy '
               'and more muscle without going to a full skid steer.'),
        bullets=['Kubota 25 HP diesel', '580 kg max lift / 400 kg rated operating load', 'Rubber tracks',
                 'Stand-on platform with full visibility to the attachment', 'Quick-hitch attachments'],
        uses=['Landscape construction', 'Site clean-up and material handling', 'Trenching and augering', 'Daily hire work'],
        spin_n=6,
    ),
    dict(
        key='HM1000T', slug='hm-1000t', name='HM 1000T', colour='orange',
        type='Stand-on tracked mini loader', cls='Mini loader',
        tagline='Our biggest stand-on loader — 650 kg lift, Kubota diesel.',
        price=31999, price_note='inc. GST, with standard bucket',
        engine='Kubota 25 HP diesel',
        specs=[('Engine', 'Kubota 25 HP diesel'), ('Operating weight', '1,550 kg'),
               ('Rated operating load', '450 kg'), ('Maximum lift capacity', '650 kg'),
               ('Undercarriage', 'Rubber tracks'), ('Operator position', 'Stand-on platform'),
               ('Standard attachment', 'General purpose bucket'), ('Optional', 'Multi bucket, auger, stump grinder')],
        blurb=('The HM 1000T is the top of the stand-on range: Kubota 25 HP diesel, 1,550 kg operating weight '
               'and a 650 kg lift. It moves pallets of pavers and full buckets of soil while still going '
               'where a skid steer can\'t.'),
        bullets=['Kubota 25 HP diesel', '650 kg max lift / 450 kg rated operating load', '1,550 kg operating weight',
                 'Rubber tracks', 'Full attachment range'],
        uses=['Heavier landscaping and paving', 'Builders and civil subcontractors', 'Nursery and material yards', 'Premium hire fleets'],
        spin_n=6,
    ),
    dict(
        key='HM1500S', slug='hm-1500s', name='HM 1500S', colour='white',
        type='Skid steer loader', cls='Skid steer',
        tagline='Full-size wheeled skid steer with enclosed cab and 0.5 m³ bucket.',
        price=74999, price_note='inc. GST, with standard bucket',
        engine='Yanmar 43 kW diesel',
        specs=[('Engine', 'Yanmar 43 kW diesel'), ('Operating weight', '3,200 kg'),
               ('Bucket capacity', '0.5 m³'), ('Drive', 'Wheeled (tracked versions available)'),
               ('Cab', 'Enclosed cab, joystick controls'), ('Standard attachment', 'Heavy-duty bucket'),
               ('Optional', 'Multi bucket, auger, stump grinder')],
        blurb=('The HM 1500S is a full-size skid steer: Yanmar 43 kW diesel, 3,200 kg operating weight, '
               'a 0.5 m³ bucket and an enclosed cab with joystick controls. Built for site work, bulk earthmoving '
               'and loading, and backed by the same 5 year / 200 hour warranty as the rest of the range.'),
        bullets=['Yanmar 43 kW diesel', 'Enclosed cab with joystick controls', '0.5 m³ heavy-duty bucket',
                 '3,200 kg operating weight', 'Wheeled — tracked versions available on request'],
        uses=['Construction and civil sites', 'Bulk material handling and loading', 'Farm and yard work', 'Demolition clean-up'],
        spin_n=9,
    ),
    dict(
        key='HME30T', slug='hme-30t', name='HME 30T', colour='white/red',
        type='Mini excavator', cls='Excavator',
        tagline='2.8 tonne class mini excavator with enclosed cab and dozer blade.',
        price=44999, price_note='inc. GST',
        engine='Yanmar 24 HP diesel',
        specs=[('Engine', 'Yanmar 24 HP diesel'), ('Operating weight', '2,780 kg'), ('Class', '2.8 tonne'),
               ('Cab', 'Enclosed cab'), ('Blade', 'Dozer blade'), ('Undercarriage', 'Rubber tracks'),
               ('Standard attachment', 'Digging bucket'), ('Optional', 'Additional buckets and auger on request')],
        blurb=('The HME 30T is a 2.8 tonne class mini excavator with a Yanmar 24 HP diesel, enclosed cab and '
               'dozer blade — the trenching, footing and site-prep machine for builders, plumbers and landscapers. '
               'Sized to trailer behind a 3.5 t-rated ute.'),
        bullets=['Yanmar 24 HP diesel', 'Enclosed cab', 'Dozer blade for backfilling and levelling',
                 '2,780 kg operating weight', 'Rubber tracks'],
        uses=['Trenching and footings', 'Plumbing and drainage', 'Pool and site excavation', 'Landscaping and retaining walls'],
        spin_n=7,
    ),
]

BY_KEY = {m['key']: m for m in MACHINES}


def price_str(p):
    return f'${p:,}'
