import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from nltk.tag import pos_tag
from nltk.chunk import ne_chunk
import re
from collections import Counter
import spacy
from string import punctuation
import requests
import json

# Import the logging backend
from logging_backend import log_interaction

# Download required NLTK data
nltk.download('punkt_tab', quiet=True)
nltk.download('stopwords', quiet=True)
nltk.download('averaged_perceptron_tagger', quiet=True)
nltk.download('maxent_ne_chunker', quiet=True)
nltk.download('words', quiet=True)

# Load spaCy model for more advanced NLP
try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    print("spaCy model not found. Please install with: python -m spacy download en_core_web_sm")
    nlp = None

class ContentProcessor:
    def __init__(self, llama_endpoint="http://127.0.0.1:1234"):
        self.stop_words = set(stopwords.words('english'))
        self.llama_endpoint = llama_endpoint
        
    def call_llama(self, prompt, max_tokens=512):
        """
        Call the local Llama model and log the interaction
        """
        headers = {
            'Content-Type': 'application/json'
        }
        
        data = {
            "model": "llama-3.2-3b-instruct",  # Specify the model
            "messages": [
                {"role": "user", "content": prompt}
            ],
            "max_tokens": max_tokens,
            "temperature": 0.3  # Lower temperature for more consistent results
        }
        
        try:
            # Log the prompt before sending
            log_interaction(prompt, "REQUEST_SENT")
            
            response = requests.post(
                f"{self.llama_endpoint}/v1/chat/completions",
                headers=headers,
                data=json.dumps(data)
            )
            
            if response.status_code == 200:
                result = response.json()
                response_text = result['choices'][0]['message']['content'].strip()
                
                # Log the actual response
                log_interaction(prompt, response_text)
                
                return response_text
            else:
                error_msg = f"Error {response.status_code}: {response.text}"
                log_interaction(prompt, error_msg)
                print(f"Error calling Llama: {response.status_code}, {response.text}")
                return None
        except Exception as e:
            error_msg = f"Exception: {str(e)}"
            log_interaction(prompt, error_msg)
            print(f"Exception calling Llama: {e}")
            return None
    
    def extract_key_sentences(self, text, max_sentences=15):
        """
        Use Llama to extract key sentences from the text
        """
        prompt = f"""
        Extract the {max_sentences} most important sentences from the following text. 
        Return each sentence on a new line with no numbering or additional text.

        Text: {text[:3000]}  # Limit text length to prevent token issues
        """
        
        result = self.call_llama(prompt, max_tokens=1024)
        
        if result:
            sentences = [s.strip() for s in result.split('\n') if s.strip() and not s.startswith('#')]
            # Filter out any empty strings or numbering
            sentences = [s for s in sentences if s and not re.match(r'^\d+\.', s)]
            return sentences[:max_sentences]
        else:
            # Fallback to NLTK method if Llama fails
            return self._nltk_extract_key_sentences(text, max_sentences)
    
    def _nltk_extract_key_sentences(self, text, max_sentences=15):
        """
        Fallback method using NLTK
        """
        sentences = sent_tokenize(text)
        
        # Remove empty sentences
        sentences = [s.strip() for s in sentences if s.strip()]
        
        if len(sentences) <= max_sentences:
            return sentences
            
        # Calculate word frequencies
        words = word_tokenize(text.lower())
        words = [w for w in words if w.isalnum() and w not in self.stop_words]
        freq_dist = Counter(words)
        
        # Score sentences based on word frequency and position
        sentence_scores = []
        for i, sentence in enumerate(sentences):
            words_in_sent = word_tokenize(sentence.lower())
            words_in_sent = [w for w in words_in_sent if w.isalnum() and w not in self.stop_words]
            
            if not words_in_sent:
                sentence_scores.append(0)
                continue
                
            # Higher score for sentences at beginning and end
            position_score = 1.0
            if i < len(sentences) * 0.1:  # First 10%
                position_score = 1.5
            elif i > len(sentences) * 0.9:  # Last 10%
                position_score = 1.2
            
            score = (sum(freq_dist[word] for word in words_in_sent) / len(words_in_sent)) * position_score
            sentence_scores.append(score)
        
        # Get top sentences
        top_indices = sorted(range(len(sentence_scores)), 
                            key=lambda i: sentence_scores[i], 
                            reverse=True)[:max_sentences]
        
        # Preserve original order
        top_indices.sort()
        return [sentences[i] for i in top_indices]
    
    def identify_headings(self, text):
        """
        Use Llama to identify potential headings from the text
        """
        prompt = f"""
        Identify 7 key headings/topics from the following text. 
        These should be concise titles that represent major themes.
        Return each heading on a new line with no numbering or additional text.

        Text: {text[:2000]}
        """
        
        result = self.call_llama(prompt, max_tokens=512)
        
        if result:
            headings = [h.strip() for h in result.split('\n') if h.strip() and not h.startswith('#')]
            # Filter out any empty strings or numbering
            headings = [h for h in headings if h and not re.match(r'^\d+\.', h)]
            return headings[:7]  # Return more headings
        else:
            # Fallback to NLTK method if Llama fails
            return self._nltk_identify_headings(text)
    
    def _nltk_identify_headings(self, text):
        """
        Fallback method using NLTK
        """
        lines = text.split('\n')
        headings = []
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
                
            # Check for common heading patterns
            if 5 < len(line) < 100:  # Reasonable heading length
                # Check for title case or all caps
                if line.isupper() or self._is_title_case(line):
                    headings.append(line)
                    
        # If no headings found, use NLP to identify key phrases
        if not headings and nlp:
            doc = nlp(text)
            # Extract noun phrases as potential headings
            noun_phrases = [chunk.text for chunk in doc.noun_chunks if len(chunk.text.split()) <= 5]
            headings = noun_phrases[:7]  # Return more headings
        else:
            # Fallback: extract first sentences as headings
            sentences = sent_tokenize(text)
            headings = [s for s in sentences[:7] if len(s) < 100]  # More headings
        
        return headings[:7]  # Return more headings
    
    def _is_title_case(self, text):
        """
        Check if text follows title case pattern
        """
        words = text.split()
        if len(words) < 2:
            return False
            
        for word in words:
            if word[0].isalpha() and not word[0].isupper():
                return False
        return True
    
    def clean_sentence(self, sentence):
        """
        Clean and improve sentence readability
        """
        # Remove extra whitespace
        sentence = re.sub(r'\s+', ' ', sentence).strip()
        
        # Fix common issues like missing spaces after periods
        sentence = re.sub(r'\.([A-Z])', r'. \1', sentence)
        
        # Capitalize first letter
        if sentence:
            sentence = sentence[0].upper() + sentence[1:]
        
        return sentence
    
    def refine_content(self, content):
        """
        Use Llama to refine content for better presentation
        """
        if not content:
            return []
        
        # Join content into a single text for processing
        text_to_refine = " ".join(content[:10])  # Limit to first 10 items to prevent token issues
        
        prompt = f"""
        Improve the following text for a presentation slide. 
        Make it more concise, clear, and impactful. Remove redundant information and fix any grammatical issues.
        Return each refined point on a new line with no numbering or additional text.

        Original Text: {text_to_refine}
        """
        
        result = self.call_llama(prompt, max_tokens=1024)
        
        if result:
            refined_content = [self.clean_sentence(s.strip()) for s in result.split('\n') if s.strip() and not s.startswith('#')]
            # Filter out any empty strings or numbering
            refined_content = [s for s in refined_content if s and not re.match(r'^\d+\.', s)]
            return refined_content
        else:
            # Fallback to basic cleaning if Llama fails
            return [self.clean_sentence(s) for s in content]
    
    def create_slide_structure(self, text):
        """
        Create a structured presentation format with improved formatting using Llama
        """
        headings = self.identify_headings(text)
        key_sentences = self.extract_key_sentences(text)
        
        # Refine content
        refined_sentences = self.refine_content(key_sentences)
        
        # Create slide structure
        slides = []
        
        # Title slide - use first heading or generate from text
        if headings:
            title = headings[0]
        else:
            # Generate title from text using Llama
            prompt = f"""
            Generate a concise and compelling presentation title for the following content:
            {text[:500]}  # Limit to first 500 characters
            
            Title:
            """
            title = self.call_llama(prompt, max_tokens=100) or "Presentation"
        
        slides.append({
            'title': title,
            'content': [],
            'type': 'title'
        })
        
        # Content slides - allow more content per slide
        sentences_per_slide = max(2, len(refined_sentences) // min(6, max(2, len(refined_sentences)//3)))
        
        for i in range(0, len(refined_sentences), sentences_per_slide):
            chunk = refined_sentences[i:i+sentences_per_slide]
            
            # Create slide title using Llama
            chunk_text = " ".join(chunk[:3])  # Use first 3 sentences to generate title
            if i < len(headings) and i > 0:
                slide_title = headings[i]
            else:
                prompt = f"""
                Generate a concise slide title for the following content:
                {chunk_text}
                
                Title:
                """
                slide_title = self.call_llama(prompt, max_tokens=100) or f"Content Slide {len(slides)}"
            
            slides.append({
                'title': slide_title,
                'content': chunk,
                'type': 'content'
            })
        
        # Ensure at least 2 slides (title + 1 content) if we have content
        if len(slides) == 1 and refined_sentences:
            # Add at least one content slide
            slides.append({
                'title': "Key Points",
                'content': refined_sentences[:5],  # First 5 sentences
                'type': 'content'
            })
        
        return slides