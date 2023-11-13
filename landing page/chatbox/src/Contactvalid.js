import { useFormik } from 'formik';
import React, { useState } from 'react';


const validate = values => {
  const errors = {};

  if (!values.first_name) {
    errors.first_name = 'Required';
  }

  if (!values.last_name) {
    errors.last_name = 'Required';
  }

  if (!values.email) {
    errors.email = 'Required';
  } else if (!/^[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}$/i.test(values.email)) {
    errors.email = 'Invalid email address';
  }

  if (!values.number) {
    errors.number = 'Required';
  } else if (!/^\+\d{3}\s\d+$/.test(values.number)) {
    errors.number = 'Invalid phone number';
  }
  if (!values.text) {
    errors.text = 'Required';
  }

  return errors;
};
const Contactvalid = () => {
  const formik = useFormik({
    initialValues: {
      first_name: '',
      last_name: '',
      email: '',
      number: '',
      text:'',
    },
    validate,
    onSubmit: values => {
      // Action à effectuer lors de la soumission du formulaire
      console.log(values);
    },
  });
  const [selectedCountry, setSelectedCountry] = useState('');
  const [phoneNumber, setPhoneNumber] = useState('');

  const countryCodes = {
    AF: '+93',
    AL: '+355',
    DZ: '+213',
    AS: '+1-684',
    AD: '+376',
    AO: '+244',
    AI: '+1-264',
    AG: '+1-268',
    AR: '+54',
    AM: '+374',
    AW: '+297',
    AU: '+61',
    AT: '+43',
    AZ: '+994',
    BS: '+1-242',
    BH: '+973',
    BD: '+880',
    BB: '+1-246',
    BY: '+375',
    BE: '+32',
    BZ: '+501',
    BJ: '+229',
    BM: '+1-441',
    BT: '+975',
    BO: '+591',
    BA: '+387',
    BW: '+267',
    BR: '+55',
    IO: '+246',
    VG: '+1-284',
    BN: '+673',
    BG: '+359',
    BF: '+226',
    BI: '+257',
    KH: '+855',
    CM: '+237',
    CA: '+1',
    CV: '+238',
    KY: '+1-345',
    CF: '+236',
    TD: '+235',
    CL: '+56',
    CN: '+86',
    CX: '+61',
    CC: '+61',
    CO: '+57',
    KM: '+269',
    CK: '+682',
    CR: '+506',
    HR: '+385',
    CU: '+53',
    CW: '+599',
    CY: '+357',
    CZ: '+420',
    CD: '+243',
    DK: '+45',
    DJ: '+253',
    DM: '+1-767',
    DO: '+1-809',
    TL: '+670',
    EC: '+593',
    EG: '+20',
    SV: '+503',
    GQ: '+240',
    ER: '+291',
    EE: '+372',
    ET: '+251',
    FK: '+500',
    FO: '+298',
    FJ: '+679',
    FI: '+358',
    FR: '+33',
    PF: '+689',
    GA: '+241',
    GM: '+220',
    GE: '+995',
    DE: '+49',
    GH: '+233',
    GI: '+350',
    GR: '+30',
    GL: '+299',
    GD: '+1-473',
    GU: '+1-671',
    GT: '+502',
    GG: '+44-1481',
    GN: '+224',
    GW: '+245',
    GY: '+592',
    HT: '+509',
    HN: '+504',
    HK: '+852',
    HU: '+36',
    IS: '+354',
    IN: '+91',
    ID: '+62',
    IR: '+98',
    IQ: '+964',
    IE: '+353',
    IM: '+44-1624',
    IL: '+972',
    IT: '+39',
    CI: '+225',
    JM: '+1-876',
    JP: '+81',
    JE: '+44-1534',
    JO: '+962',
    KZ: '+7',
    KE: '+254',
    KI: '+686',
    XK: '+383',
    KW: '+965',
    KG: '+996',
    LA: '+856',
    LV: '+371',
    LB: '+961',
    LS: '+266',
    LR: '+231',
    LY: '+218',
    LI: '+423',
    LT: '+370',
    LU: '+352',
    MO: '+853',
    MK: '+389',
    MG: '+261',
    MW: '+265',
    MY: '+60',
    MV: '+960',
    ML: '+223',
    MT: '+356',
    MH: '+692',
    MR: '+222',
    MU: '+230',
    YT: '+262',
    MX: '+52',
    FM: '+691',
    MD: '+373',
    MC: '+377',
    MN: '+976',
    ME: '+382',
    MS: '+1-664',
    MA: '+212',
    MZ: '+258',
    MM: '+95',
    NA: '+264',
    NR: '+674',
    NP: '+977',
    NL: '+31',
    NC: '+687',
    NZ: '+64',
    NI: '+505',
    NE: '+227',
    NG: '+234',
    NU: '+683',
    KP: '+850',
    MP: '+1-670',
    NO: '+47',
    OM: '+968',
    PK: '+92',
    PW: '+680',
    PS: '+970',
    PA: '+507',
    PG: '+675',
    PY: '+595',
    PE: '+51',
    PH: '+63',
    PN: '+64',
    PL: '+48',
    PT: '+351',
    PR: '+1-787',
    QA: '+974',
    CG: '+242',
    RO: '+40',
    RU: '+7',
    RW: '+250',
    BL: '+590',
    SH: '+290',
    KN: '+1-869',
    LC: '+1-758',
    MF: '+590',
    PM: '+508',
    VC: '+1-784',
    WS: '+685',
    SM: '+378',
    ST: '+239',
    SA: '+966',
    SN: '+221',
    RS: '+381',
    SC: '+248',
    SL: '+232',
    SG: '+65',
    SX: '+1-721',
    SK: '+421',
    SI: '+386',
    SB: '+677',
    SO: '+252',
    ZA: '+27',
    KR: '+82',
    SS: '+211',
    ES: '+34',
    LK: '+94',
    SD: '+249',
    SR: '+597',
    SJ: '+47',
    SZ: '+268',
    SE: '+46',
    CH: '+41',
    SY: '+963',
    TW: '+886',
    TJ: '+992',
    TZ: '+255',
    TH: '+66',
    TG: '+228',
    TK: '+690',
    TO: '+676',
    TT: '+1-868',
    TN: '+216',
    TR: '+90',
    TM: '+993',
    TC: '+1-649',
    TV: '+688',
    VI: '+1-340',
    UG: '+256',
    UA: '+380',
    AE: '+971',
    GB: '+44',
    US: '+1',
    UY: '+598',
    UZ: '+998',
    VU: '+678',
    VA: '+39-06',
    VE: '+58',
    VN: '+84',
    WF: '+681',
    EH: '+212',
    YE: '+967',
    ZM: '+260',
    ZW: '+263',
  };

  const handleCountryChange = (event) => {
    const countryCode = event.target.value;
    setSelectedCountry(countryCode);
    setPhoneNumber(countryCodes[countryCode]);
  };
  
  const getCountryName = (countryCode) => {
    switch (countryCode) {
      case 'AF':
        return 'Afghanistan';
      case 'AL':
        return 'Albania';
      case 'DZ':
        return 'Algeria';
      case 'AS':
        return 'American Samoa';
      case 'AD':
        return 'Andorra';
      case 'AO':
        return 'Angola';
      case 'AI':
        return 'Anguilla';
      case 'AQ':
        return 'Antarctica';
      case 'AG':
        return 'Antigua and Barbuda';
      case 'AR':
        return 'Argentina';
      case 'AM':
        return 'Armenia';
      case 'AW':
        return 'Aruba';
      case 'AU':
        return 'Australia';
      case 'AT':
        return 'Austria';
      case 'AZ':
        return 'Azerbaijan';
      case 'BS':
        return 'Bahamas';
      case 'BH':
        return 'Bahrain';
      case 'BD':
        return 'Bangladesh';
      case 'BB':
        return 'Barbados';
      case 'BY':
        return 'Belarus';
      case 'BE':
        return 'Belgium';
      case 'BZ':
        return 'Belize';
      case 'BJ':
        return 'Benin';
      case 'BM':
        return 'Bermuda';
      case 'BT':
        return 'Bhutan';
      case 'BO':
        return 'Bolivia';
      case 'BA':
        return 'Bosnia and Herzegovina';
      case 'BW':
        return 'Botswana';
      case 'BV':
        return 'Bouvet Island';
      case 'BR':
        return 'Brazil';
      case 'IO':
        return 'British Indian Ocean Territory';
      case 'BN':
        return 'Brunei Darussalam';
      case 'BG':
        return 'Bulgaria';
      case 'BF':
        return 'Burkina Faso';
      case 'BI':
        return 'Burundi';
      case 'KH':
        return 'Cambodia';
      case 'CM':
        return 'Cameroon';
      case 'CA':
        return 'Canada';
      case 'CV':
        return 'Cape Verde';
      case 'KY':
        return 'Cayman Islands';
      case 'CF':
        return 'Central African Republic';
      case 'TD':
        return 'Chad';
      case 'CL':
        return 'Chile';
      case 'CN':
        return 'China';
      case 'CX':
        return 'Christmas Island';
      case 'CC':
        return 'Cocos (Keeling) Islands';
      case 'CO':
        return 'Colombia';
      case 'KM':
        return 'Comoros';
      case 'CG':
        return 'Congo';
      case 'CD':
        return 'Congo, the Democratic Republic of the';
      case 'CK':
        return 'Cook Islands';
      case 'CR':
        return 'Costa Rica';
      case 'CI':
        return 'Côte d\'Ivoire';
      case 'HR':
        return 'Croatia';
      case 'CU':
        return 'Cuba';
      case 'CY':
        return 'Cyprus';
      case 'CZ':
        return 'Czech Republic';
      case 'DK':
        return 'Denmark';
      case 'DJ':
        return 'Djibouti';
      case 'DM':
        return 'Dominica';
      case 'DO':
        return 'Dominican Republic';
      case 'EC':
        return 'Ecuador';
      case 'EG':
        return 'Egypt';
      case 'SV':
        return 'El Salvador';
      case 'GQ':
        return 'Equatorial Guinea';
      case 'ER':
        return 'Eritrea';
      case 'EE':
        return 'Estonia';
      case 'ET':
        return 'Ethiopia';
      case 'FK':
        return 'Falkland Islands (Malvinas)';
      case 'FO':
        return 'Faroe Islands';
      case 'FJ':
        return 'Fiji';
      case 'FI':
        return 'Finland';
      case 'FR':
        return 'France';
      case 'GF':
        return 'French Guiana';
      case 'PF':
        return 'French Polynesia';
      case 'TF':
        return 'French Southern Territories';
      case 'GA':
        return 'Gabon';
      case 'GM':
        return 'Gambia';
      case 'GE':
        return 'Georgia';
      case 'DE':
        return 'Germany';
      case 'GH':
        return 'Ghana';
      case 'GI':
        return 'Gibraltar';
      case 'GR':
        return 'Greece';
      case 'GL':
        return 'Greenland';
      case 'GD':
        return 'Grenada';
      case 'GP':
        return 'Guadeloupe';
      case 'GU':
        return 'Guam';
      case 'GT':
        return 'Guatemala';
      case 'GG':
        return 'Guernsey';
      case 'GN':
        return 'Guinea';
      case 'GW':
        return 'Guinea-Bissau';
      case 'GY':
        return 'Guyana';
      case 'HT':
        return 'Haiti';
      case 'HM':
        return 'Heard Island and McDonald Islands';
      case 'VA':
        return 'Holy See (Vatican City State)';
      case 'HN':
        return 'Honduras';
      case 'HK':
        return 'Hong Kong';
      case 'HU':
        return 'Hungary';
      case 'IS':
        return 'Iceland';
      case 'IN':
        return 'India';
      case 'ID':
        return 'Indonesia';
      case 'IR':
        return 'Iran, Islamic Republic of';
      case 'IQ':
        return 'Iraq';
      case 'IE':
        return 'Ireland';
      case 'IM':
        return 'Isle of Man';
      case 'IL':
        return 'Israel';
      case 'IT':
        return 'Italy';
      case 'JM':
        return 'Jamaica';
      case 'JP':
        return 'Japan';
      case 'JE':
        return 'Jersey';
      case 'JO':
        return 'Jordan';
      case 'KZ':
        return 'Kazakhstan';
      case 'KE':
        return 'Kenya';
      case 'KI':
        return 'Kiribati';
      case 'KP':
        return 'Korea, Democratic People\'s Republic of';
      case 'KR':
        return 'Korea, Republic of';
      case 'KW':
        return 'Kuwait';
      case 'KG':
        return 'Kyrgyzstan';
      case 'LA':
        return 'Lao People\'s Democratic Republic';
      case 'LV':
        return 'Latvia';
      case 'LB':
        return 'Lebanon';
      case 'LS':
        return 'Lesotho';
      case 'LR':
        return 'Liberia';
      case 'LY':
        return 'Libya';
      case 'LI':
        return 'Liechtenstein';
      case 'LT':
        return 'Lithuania';
      case 'LU':
        return 'Luxembourg';
      case 'MO':
        return 'Macao';
      case 'MK':
        return 'Macedonia, the Former Yugoslav Republic of';
      case 'MG':
        return 'Madagascar';
      case 'MW':
        return 'Malawi';
      case 'MY':
        return 'Malaysia';
      case 'MV':
        return 'Maldives';
      case 'ML':
        return 'Mali';
      case 'MT':
        return 'Malta';
      case 'MH':
        return 'Marshall Islands';
      case 'MQ':
        return 'Martinique';
      case 'MR':
        return 'Mauritania';
      case 'MU':
        return 'Mauritius';
      case 'YT':
        return 'Mayotte';
      case 'MX':
        return 'Mexico';
      case 'FM':
        return 'Micronesia, Federated States of';
      case 'MD':
        return 'Moldova, Republic of';
      case 'MC':
        return 'Monaco';
      case 'MN':
        return 'Mongolia';
      case 'ME':
        return 'Montenegro';
      case 'MS':
        return 'Montserrat';
      case 'MA':
        return 'Morocco';
      case 'MZ':
        return 'Mozambique';
      case 'MM':
        return 'Myanmar';
      case 'NA':
        return 'Namibia';
      case 'NR':
        return 'Nauru';
      case 'NP':
        return 'Nepal';
      case 'NL':
        return 'Netherlands';
      case 'NC':
        return 'New Caledonia';
      case 'NZ':
        return 'New Zealand';
      case 'NI':
        return 'Nicaragua';
      case 'NE':
        return 'Niger';
      case 'NG':
        return 'Nigeria';
      case 'NU':
        return 'Niue';
      case 'NF':
        return 'Norfolk Island';
      case 'MP':
        return 'Northern Mariana Islands';
      case 'NO':
        return 'Norway';
      case 'OM':
        return 'Oman';
      case 'PK':
        return 'Pakistan';
      case 'PW':
        return 'Palau';
      case 'PS':
        return 'Palestine, State of';
      case 'PA':
        return 'Panama';
      case 'PG':
        return 'Papua New Guinea';
      case 'PY':
        return 'Paraguay';
      case 'PE':
        return 'Peru';
      case 'PH':
        return 'Philippines';
      case 'PN':
        return 'Pitcairn';
      case 'PL':
        return 'Poland';
      case 'PT':
        return 'Portugal';
      case 'PR':
        return 'Puerto Rico';
      case 'QA':
        return 'Qatar';
      case 'RE':
        return 'Réunion';
      case 'RO':
        return 'Romania';
      case 'RU':
        return 'Russian Federation';
      case 'RW':
        return 'Rwanda';
      case 'BL':
        return 'Saint Barthélemy';
      case 'SH':
        return 'Saint Helena, Ascension and Tristan da Cunha';
      case 'KN':
        return 'Saint Kitts and Nevis';
      case 'LC':
        return 'Saint Lucia';
      case 'MF':
        return 'Saint Martin (French part)';
      case 'PM':
        return 'Saint Pierre and Miquelon';
      case 'VC':
        return 'Saint Vincent and the Grenadines';
      case 'WS':
        return 'Samoa';
      case 'SM':
        return 'San Marino';
      case 'ST':
        return 'Sao Tome and Principe';
      case 'SA':
        return 'Saudi Arabia';
      case 'SN':
        return 'Senegal';
      case 'RS':
        return 'Serbia';
      case 'SC':
        return 'Seychelles';
      case 'SL':
        return 'Sierra Leone';
      case 'SG':
        return 'Singapore';
      case 'SX':
        return 'Sint Maarten (Dutch part)';
      case 'SK':
        return 'Slovakia';
      case 'SI':
        return 'Slovenia';
      case 'SB':
        return 'Solomon Islands';
      case 'SO':
        return 'Somalia';
      case 'ZA':
        return 'South Africa';
      case 'GS':
        return 'South Georgia and the South Sandwich Islands';
      case 'SS':
        return 'South Sudan';
      case 'ES':
        return 'Spain';
      case 'LK':
        return 'Sri Lanka';
      case 'SD':
        return 'Sudan';
      case 'SR':
        return 'Suriname';
      case 'SJ':
        return 'Svalbard and Jan Mayen';
      case 'SZ':
        return 'Swaziland';
      case 'SE':
        return 'Sweden';
      case 'CH':
        return 'Switzerland';
      case 'SY':
        return 'Syrian Arab Republic';
      case 'TW':
        return 'Taiwan, Province of China';
      case 'TJ':
        return 'Tajikistan';
      case 'TZ':
        return 'Tanzania, United Republic of';
      case 'TH':
        return 'Thailand';
      case 'TL':
        return 'Timor-Leste';
      case 'TG':
        return 'Togo';
      case 'TK':
        return 'Tokelau';
      case 'TO':
        return 'Tonga';
      case 'TT':
        return 'Trinidad and Tobago';
      case 'TN':
        return 'Tunisia';
      case 'TR':
        return 'Turkey';
      case 'TM':
        return 'Turkmenistan';
      case 'TC':
        return 'Turks and Caicos Islands';
      case 'TV':
        return 'Tuvalu';
      case 'UG':
        return 'Uganda';
      case 'UA':
        return 'Ukraine';
      case 'AE':
        return 'United Arab Emirates';
      case 'GB':
        return 'United Kingdom';
      case 'US':
        return 'United States';
      case 'UM':
        return 'United States Minor Outlying Islands';
      case 'UY':
        return 'Uruguay';
      case 'UZ':
        return 'Uzbekistan';
      case 'VU':
        return 'Vanuatu';
      case 'VE':
        return 'Venezuela, Bolivarian Republic of';
      case 'VN':
        return 'Viet Nam';
      case 'VG':
        return 'Virgin Islands, British';
      case 'VI':
        return 'Virgin Islands, U.S.';
      case 'WF':
        return 'Wallis and Futuna';
      case 'EH':
        return 'Western Sahara';
      case 'YE':
        return 'Yemen';
      case 'ZM':
        return 'Zambia';
      case 'ZW':
        return 'Zimbabwe';
      default:
        return '';
    }
  };
  return (
    <form onSubmit={formik.handleSubmit}>
      <input
        type="text"
        name="first_name"
        className={`intro-x login__input form-control py-3 px-4 block ${
          formik.errors.first_name && formik.touched.first_name ? 'is-invalid' : ''
        }`}
        placeholder="First Name"
        value={formik.values.first_name}
        onChange={formik.handleChange}
        onBlur={formik.handleBlur}
      />
      {formik.errors.first_name && formik.touched.first_name && (
        <div className="invalid-feedback">{formik.errors.first_name}</div>
      )}

      <input
        type="text"
        name="last_name"
        className={`intro-x login__input form-control py-3 px-4 block ${
          formik.errors.last_name && formik.touched.last_name ? 'is-invalid' : ''
        }`}
        placeholder="Last Name"
        value={formik.values.last_name}
        onChange={formik.handleChange}
        onBlur={formik.handleBlur}
      />
      {formik.errors.last_name && formik.touched.last_name && (
        <div className="invalid-feedback">{formik.errors.last_name}</div>
      )}
      <input
        type="text"
        name="email"
        className={`intro-x login__input form-control py-3 px-4 block ${
          formik.errors.email && formik.touched.email ? 'is-invalid' : ''
        }`}
        placeholder="Email"
        value={formik.values.email}
        onChange={formik.handleChange}
        onBlur={formik.handleBlur}
      />
      {formik.errors.email && formik.touched.email && (
        <div className="invalid-feedback">{formik.errors.email}</div>
      )}
       <select
        class="intro-x login__input form-control py-3 px-4 block mt-4 w-75 "
        name="select"
        value={selectedCountry}
        onChange={handleCountryChange}
      >
        <option disabled value="">Select Country</option>
        {Object.entries(countryCodes).map(([countryCode]) => (
  <option key={countryCode} value={countryCode}>{getCountryName(countryCode)}</option>
))}
      </select>
      <input
        class="intro-x login__input form-control py-3 px-4 block mt-4 w-75  "
        name="number"
        placeholder="Phone"
        type="tel"
        inputMode="tel"
        autoComplete="tel"
        value={`${phoneNumber}`}
        onChange={(event) => setPhoneNumber(event.target.value)}
      />
    <textarea
  type="text"
  name="text"
  className={`intro-x login__input form-control py-3 px-4 block ${
    formik.errors.text && formik.touched.text ? 'is-invalid' : ''
  }`}
  placeholder="Enter your Message"
  value={formik.values.text}
  onChange={formik.handleChange}
  onBlur={formik.handleBlur}
></textarea>
{formik.errors.text && formik.touched.text && (
  <div className="invalid-feedback">{formik.errors.text}</div>
)}

      <button class="btn btn-primary py-3 px-4 w-full xl:w-32 xl:mr-3 align-top" type="submit">Register</button>
    </form>
  );
};
export default Contactvalid;