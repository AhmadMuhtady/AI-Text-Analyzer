from text_validation import text_validation
from calling_model import analyze_text
from summary_length_validation import summary_length_validation


text = """
The Vietnam War (c. 1955[A 1] – 30 April 1975) was an armed conflict in Vietnam, Laos, and Cambodia fought between North Vietnam (Democratic Republic of Vietnam) and South Vietnam (Republic of Vietnam) and their allies. North Vietnam was supported by the Soviet Union and China, while South Vietnam was supported by the United States and other anti-communist nations. The conflict was the second of the Indochina wars and a proxy war of the Cold War. The Vietnam War was one of the postcolonial wars of national liberation, a theater in the Cold War, and a civil war, with civil warfare a defining feature from the outset.[43] Direct US military involvement escalated from 1965 until US forces were withdrawn in 1973. The fighting spilled into the Laotian and Cambodian civil wars, which ended with all three countries becoming communist in 1975.

The civil and colonial conflicts in Vietnam became internationalized in 1950.[A 5] After the defeat of the French Union in the First Indochina War, Vietnam's independence was affirmed at the 1954 Geneva Conference, but the country was divided at the 17th parallel: the Viet Minh, led by Ho Chi Minh, took control of North Vietnam, while Ngo Dinh Diem led South Vietnam, which the US assumed financial and military support for. The North Vietnamese supplied and eventually directed the Viet Cong (VC), a communist front in the south that intensified a guerrilla war from 1957. In 1958, North Vietnam invaded Laos, establishing the Ho Chi Minh trail to supply the VC insurgency. By 1961, North Vietnam was covertly sending soldiers of its People's Army of Vietnam (PAVN) to assist the southern insurgents. President John F. Kennedy increased US involvement in the early 1960s, including military advisors and aid to the Army of the Republic of Vietnam (ARVN). In 1963, Diem was killed in a US-backed ARVN military coup, which added to South Vietnam's growing instability.

Following the Gulf of Tonkin incident in 1964, the US Congress passed a resolution that gave President Lyndon B. Johnson authority to increase military presence without declaring war. Johnson launched a bombing campaign of the north and deployed combat troops, dramatically increasing deployment to 184,000 by 1966, and 536,000 by 1969. US forces relied on air supremacy and overwhelming firepower to conduct search and destroy operations in rural areas. Communist forces relied on guerrilla tactics, using the countryside and jungle as concealed base areas.

In 1968, the communists under Lê Duẩn launched the Tet Offensive, which was a tactical defeat but contributed to growing American opposition to the war. Johnson's successor, Richard Nixon, began "Vietnamization" from 1969, which saw the conflict fought by an expanded ARVN while US forces withdrew. The 1970 Cambodian coup d'état resulted in a PAVN invasion and US–ARVN counter-invasion, escalating its civil war.

With its ranks degraded by widespread drug abuse and plummeting morale, US troops had mostly withdrawn from Vietnam by 1972. However, American forces provided crucial air support to ARVN against North Vietnam's massive Easter Offensive with the Linebacker Operations. Following the 1973 Paris Peace Accords, the last American forces left. The accords were subsequently violated by North Vietnam, and bloody fighting continued until the 1975 Spring Offensive. Weakened by years of corruption and the economic troubles of South Vietnam's Thiệu regime, Saigon fell to the PAVN, marking the war's end. North and South Vietnam were officially reunified in 1976.

The war exacted an enormous cost: estimates of Vietnamese soldiers and civilians killed range from 970,000 to 3 million. Some 275,000–310,000 Cambodians, 20,000–62,000 Laotians, and 58,220 US service members died.[A 4] The war was also marked by brutal atrocities, including large-scale massacres (such as Huế and Mỹ Lai), terrorism, indiscriminate bombings, rape, torture, and persecution of ethnic minorities. 20% of South Vietnam's jungle was sprayed with toxic herbicides, which led to significant health problems.[51]

Political repression and flawed economic policies following the war would precipitate the Vietnamese boat people and the larger Indochina refugee crisis,[52] which saw millions leave Indochina, of which about 250,000 perished at sea.[53] The Khmer Rouge carried out the Cambodian genocide, and the Cambodian–Vietnamese War began in 1978. In response, China invaded Vietnam, with border conflicts lasting until 1991. Within the US, the war gave rise to Vietnam syndrome, an aversion to American overseas military involvement,[54] which, with the Watergate scandal, contributed to the crisis of confidence that affected the United States throughout the 1970s.[55]
"""

length = 'long'


def pipeline(text,length):
    try:
        text_val = text_validation(text,length)
        summarizer = analyze_text(text_val)
        summary_val = summary_length_validation(summarizer['summary'],length)

        return summarizer
    except Exception as e:
        return e




app = pipeline(text,length)


print(app)