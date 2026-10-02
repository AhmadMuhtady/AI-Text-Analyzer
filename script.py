def text_validation(txt: str , lngth: str) -> dict:
        if not isinstance(txt,str):
            raise TypeError('Text should be a string!')

        if not isinstance(lngth,str):
            raise TypeError('length should be a string!')





        cleaned_text = txt.strip()
        normalized_length = lngth.strip().lower()

        if not cleaned_text:
            raise ValueError('Text cant be empty')

        if not normalized_length or normalized_length not in ['short', 'medium', 'long']:
            raise ValueError('Text Length should be short, medium or long')



        return {'text': cleaned_text, 'length': normalized_length}


