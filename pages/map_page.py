import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

nationality_options = ["Afghan", "Albanian", "Algerian", "American", "Andorran", "Angolan", "Antiguans", "Argentinean",
                       "Armenian", "Australian", "Austrian", "Azerbaijani", "Bahamian", "Bahraini", "Bangladeshi",
                       "Barbadian", "Barbudans", "Batswana", "Belarusian", "Belgian", "Belizean", "Beninese",
                       "Bhutanese", "Bolivian", "Bosnian", "Brazilian", "British", "Bruneian", "Bulgarian", "Burkinabe",
                       "Burmese", "Burundian", "Cambodian", "Cameroonian", "Canadian", "Cape Verdean",
                       "Central African",
                       "Chadian", "Chilean", "Chinese", "Colombian", "Comoran", "Congolese", "Costa Rican", "Croatian",
                       "Cuban", "Cypriot", "Czech", "Danish", "Djibouti", "Dominican", "Dutch", "East Timorese",
                       "Ecuadorean", "Egyptian", "Emirian", "Equatorial Guinean", "Eritrean", "Estonian", "Ethiopian",
                       "Fijian", "Filipino", "Finnish", "French", "Gabonese", "Gambian", "Georgian", "German",
                       "Ghanaian", "Greek", "Grenadian", "Guatemalan", "Guinea-Bissauan", "Guinean", "Guyanese",
                       "Haitian", "Herzegovinian", "Honduran", "Hungarian", "I-Kiribati", "Icelander", "Indian",
                       "Indonesian", "Iranian", "Iraqi", "Irish", "Israeli", "Italian", "Ivorian", "Jamaican",
                       "Japanese", "Jordanian", "Kazakhstani", "Kenyan", "Kittian and Nevisian", "Kuwaiti", "Kyrgyz",
                       "Laotian", "Latvian", "Lebanese", "Liberian", "Libyan", "Liechtensteiner", "Lithuanian",
                       "Luxembourger", "Macedonian", "Malagasy", "Malawian", "Malaysian", "Maldivian", "Malian",
                       "Maltese", "Marshallese", "Mauritanian", "Mauritian", "Mexican", "Micronesian", "Moldovan",
                       "Monacan", "Mongolian", "Moroccan", "Mosotho", "Motswana", "Mozambican", "Namibian", "Nauruan",
                       "Nepalese", "New Zealander", "Ni-Vanuatu", "Nicaraguan", "Nigerian", "Nigerien", "North Korean",
                       "Northern Irish", "Norwegian", "Omani", "Pakistani", "Palauan", "Panamanian",
                       "Papua New Guinean", "Paraguayan", "Peruvian", "Polish", "Portuguese", "Qatari", "Romanian",
                       "Russian", "Rwandan", "Saint Lucian", "Salvadoran", "Samoan", "San Marinese", "Sao Tomean",
                       "Saudi", "Scottish", "Senegalese", "Serbian", "Seychellois", "Sierra Leonean", "Singaporean",
                       "Slovakian", "Slovenian", "Solomon Islander", "Somali", "South African", "South Korean",
                       "Spanish", "Sri Lankan", "Sudanese", "Surinamer", "Swazi", "Swedish", "Swiss", "Syrian",
                       "Taiwanese", "Tajik", "Tanzanian", "Thai", "Togolese", "Tongan", "Trinidadian or Tobagonian",
                       "Tunisian", "Turkish", "Tuvaluan", "Ugandan", "Ukrainian", "Uruguayan", "Uzbekistani",
                       "Venezuelan", "Vietnamese", "Welsh", "Yemenite", "Zambian", "Zimbabwean"]
nationality_options = [dict(label=nationality, value=nationality) for nationality in nationality_options]


layout = html.Div([
    # Header
    html.Div([
        html.Div([
            html.H1(children='Where to live!',
                    style={'textAlign': 'center'}
                    ),
            html.H2('In this dashboard you can indicate your preferences and \
                     navigate the map to find the perfect city for you to live')
        ],
            className='header',
            style={'padding-top': '1%'}
        )],
        className='row'
    ),
    # Body
    html.Div([
        # Navigation Bar
        html.Div([
            html.A('Home', href='/main', className='navButton'),
            html.A('Map', href='/map_page', className='navButton'),
            html.A('Compare your profile', href='/profile', className='navButton'),
            html.A('Preferences', href='/preferences', className='navButton'),
            html.A('Countries Stats', href='/countries', className='navButton')
        ],
            className='mainNav'),
        # Map Section
        html.Div([
            # Preferences
            html.Div([
                html.H4('Set your profile preferences'),
                html.Div([
                    html.A('Nationality:', className='preferencesText'),
                    dcc.Dropdown(
                        placeholder='Select Nationality',
                        options=nationality_options,
                        clearable=False,
                        className='dropdownMenu',
                    )
                ],
                    className='nationalityContainer'
                ),
                html.Div([
                    html.A('Income level:', className='preferencesText'),
                    dcc.RangeSlider(
                        id='incomeSlider',
                        min=0,
                        max=10,
                        value=[5],
                        step=1,
                        marks={0: '0',
                               5: '5',
                               10: '10'},
                        className='slider'
                    )
                ],
                    className="sliderContainer"
                ),
                html.Div([
                    html.A('Good Weather:', className='preferencesText'),
                    dcc.RangeSlider(
                        id='weatherSlider',
                        min=0,
                        max=10,
                        value=[5],
                        step=1,
                        marks={0: '0',
                               5: '5',
                               10: '10'},
                        className='slider',
                    )
                ],
                    className="sliderContainer"
                ),
                html.Div([
                    html.A('Living Cost:', className='preferencesText'),
                    dcc.RangeSlider(
                        id='livingCostSlider',
                        min=0,
                        max=10,
                        value=[5],
                        step=1,
                        marks={0: '0',
                               5: '5',
                               10: '10'},
                        className='slider'
                    )
                ],
                    className="sliderContainer"
                ),
                html.Div([
                    html.A('Internet connection:', className='preferencesText'),
                    dcc.RangeSlider(
                        id='internetSlider',
                        min=0,
                        max=10,
                        value=[5],
                        step=1,
                        marks={0: '0',
                               5: '5',
                               10: '10'},
                        className='slider'
                    )
                ],
                    className="sliderContainer"
                ),
                html.Div([
                    html.A('Nightlife:', className='preferencesText'),
                    dcc.RangeSlider(
                        id='nightlifeSlider',
                        min=0,
                        max=10,
                        value=[5],
                        step=1,
                        marks={0: '0',
                               5: '5',
                               10: '10'},
                        className='slider'
                    )
                ],
                    className="sliderContainer"
                ),
            ],
                id="preferences_div",
                className="paddings"
            ),

            html.Div([
                html.Canvas(id="map", width='900', height='400')
            ],
                id='map-div',
            )
        ],
            id='map-section',
            className='col-12'
        )
    ],
        className='body',

    )
])
