# Chefbot Usage Examples

This document provides examples of how to use Chefbot and what kind of conversations you can have.

## Getting Started

After setting up your `.env` file with your Venice AI API key, simply run:

```bash
python chefbot.py
```

## Example Conversations

### Example 1: Getting a Recipe

```
You: Can you give me a recipe for homemade pizza dough?

Chef: I'd be happy to share a fantastic homemade pizza dough recipe! This recipe makes 
enough for two 12-inch pizzas.

**Classic Pizza Dough**

Ingredients:
- 500g (4 cups) all-purpose flour / 500g bread flour
- 325ml (1⅓ cups) warm water (about 40°C/105°F)
- 2 teaspoons (7g) active dry yeast
- 2 teaspoons (10g) salt
- 1 tablespoon (15ml) olive oil
- 1 teaspoon sugar

Instructions:
1. Activate the yeast: Mix warm water, sugar, and yeast. Let stand 5-10 minutes until foamy.
2. In a large bowl, combine flour and salt.
3. Add the yeast mixture and olive oil to the flour.
4. Mix until a shaggy dough forms, then knead for 8-10 minutes until smooth and elastic.
5. Place in an oiled bowl, cover, and let rise for 1-2 hours until doubled.
6. Punch down, divide in half, and let rest 15 minutes before shaping.

The dough can be refrigerated for up to 3 days or frozen for up to 3 months!
```

### Example 2: Remembering Previous Recipes

```
You: Can you remind me of that pizza dough recipe we discussed?

Chef: Of course! Earlier I shared a classic pizza dough recipe that makes two 12-inch 
pizzas. The key ingredients are 500g flour, 325ml warm water, yeast, salt, olive oil, 
and a bit of sugar. You knead it for 8-10 minutes, let it rise for 1-2 hours, and 
then it's ready to shape. Would you like me to provide the full details again?
```

### Example 3: Ingredient Substitutions

```
You: I don't have all-purpose flour. Can I substitute something else?

Chef: Great question! You have several options:

1. **Bread flour**: This is actually ideal for pizza! It has more protein, which 
   creates a chewier crust with better structure.

2. **Whole wheat flour**: You can substitute up to 50% of the all-purpose flour 
   with whole wheat for a nuttier flavor and more fiber. Use 100% whole wheat for 
   a heartier crust, but add a bit more water as it absorbs more liquid.

3. **00 Flour**: This Italian flour creates an authentic Neapolitan-style crust 
   that's tender and crispy.

Which would you like to try?
```

### Example 4: Cooking Techniques

```
You: How do I know when my bread is done baking?

Chef: Excellent question! There are several reliable methods to check if your bread 
is done:

1. **Internal Temperature**: The most reliable method - bread is done when the 
   internal temperature reaches 190-200°F (88-93°C) for enriched breads, or 
   200-210°F (93-99°C) for lean breads. Use an instant-read thermometer.

2. **Tap Test**: Tap the bottom of the loaf - it should sound hollow when fully baked.

3. **Visual Cues**: The crust should be golden brown (or the color specified in 
   your recipe).

4. **Firmness**: The loaf should feel firm and set, not soft or squishy.

Always let bread cool completely before slicing - this allows the structure to set!
```

### Example 5: Meal Planning

```
You: I need ideas for a dinner party for 6 people. I want to impress!

Chef: How exciting! Let me suggest a menu that will definitely impress your guests:

**Appetizer**: Caprese Skewers with balsamic reduction
- Easy to prepare ahead, elegant presentation

**Main Course**: Pan-seared salmon with lemon butter sauce, roasted asparagus, 
and garlic herb potatoes
- Can partially prep ahead, impressive but manageable

**Dessert**: Individual chocolate lava cakes
- Can be prepared and refrigerated, baked just before serving

This menu has great variety, sophisticated flavors, and strategic timing so you're 
not overwhelmed. Would you like the detailed recipes for any of these dishes?
```

## Commands

- **Regular chat**: Just type your question or message
- **clear**: Clear conversation history
- **quit** or **exit**: End the session

## Tips for Best Results

1. **Be specific**: The more details you provide, the better the chef can help
2. **Ask follow-ups**: Don't hesitate to ask for clarification or more details
3. **Reference previous conversations**: The bot remembers everything you've discussed
4. **Save recipes**: Share recipes with the bot, and it will remember them for future reference
5. **Ask about substitutions**: If you're missing ingredients, ask for alternatives

## Features to Explore

- Recipe development and customization
- Dietary accommodations (vegetarian, vegan, gluten-free, etc.)
- Cooking technique explanations
- Food safety and storage advice
- Ingredient substitutions
- Troubleshooting cooking problems
- Meal planning assistance
- Kitchen equipment recommendations
