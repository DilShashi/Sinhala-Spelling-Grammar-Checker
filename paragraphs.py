# paragraphs.py

def get_paragraphs():
    """
    Returns a list of dictionaries containing input and true paragraphs.

    Returns:
        List[Dict[str, str]]: A list of dictionaries with 'input_paragraph' and 'true_paragraph'.
    """
    paragraphs = [
        {
            "input_paragraph": "මම දෙඩම් කනවා. අමාලි පාසැලට යනව. අපි කෑම කනවා. කුරුල්ලෝ පියාඹනවා.",
            "true_paragraph": "මම දොඩම් කමි. අමාලි පාසැලට යයි. අපි කෑම කමු. කුරුල්ලෝ පියාඹති."
        },
        {
            "input_paragraph": "අපි ගමන යමු. අහස ලාබිණි. මල් සොඳුරුයි. ගඟ නිරවුල් ය.",
            "true_paragraph": "අපි ගමන යමු. අහස ලාබිණියි. මල් සොඳුරුයි. ගඟ නිරවුල් වේ."
        },
        {
            "input_paragraph": "සීතා පොතක් කියවයි. කුසුම් ගේ දුව යායි. සීතල රැයක් විය.",
            "true_paragraph": "සීතා පොතක් කියවයි. කුසුම්ගේ දුව යයි. සීතල රැයක් විය."
        },
        {
            "input_paragraph": "අපි පැටවුන් සොයා ගියෙමු. ගඟේ ජලය සිසිල්ය. තේනුවර බලා සිටිමු.",
            "true_paragraph": "අපි පැටවුන් සොයා ගියෙමු. ගඟේ ජලය සිසිලසය. තේනුවර බලා සිටිමු."
        },
        {
            "input_paragraph": "සඳලි මනෝරාට කතා කලා. යාළුන් එනවා. පියගැටේ සන්සුන්ය.",
            "true_paragraph": "සඳලි මනෝරාට කතා කලා. යාළුන් එනවා. පියගැටේ සන්සුන් ය."
        }
    ]
    return paragraphs