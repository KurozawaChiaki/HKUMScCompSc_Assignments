#import "template.typ": project

#show: project.with(
  title: "Unveiling Movie Magic:\nInsights into Industry Trends, Audience Preferences, and Box Office Success",
  authors: (
    (name: "-", 
    email: "-", 
    affiliation: "-", 
    postal: "", 
    phone: ""),
  )
)

= Introduction

== Foreword

The movie industry, a vibrant and ever-evolving domain, offers valuable insights into audience preferences, market dynamics, and creative trends. With an abundance of data available, analyzing movies from multiple dimensions provides opportunities to uncover factors that drive both critical acclaim and commercial success. Our project investigates the intricate relationships between industry trends, movie ratings, and box office performance, providing a comprehensive view of the film landscape.

Our analysis is structured around five core themes: a general overview of movies to establish foundational patterns; industry trends to identify shifts over time; factors influencing box office revenues; determinants of IMDb ratings; and the interplay between high ratings and high box office performance. By leveraging a rich dataset encompassing genres, ratings, revenue, release years, and other critical features, this study employs both descriptive and inferential analyses to generate actionable insights.

The findings aim to benefit stakeholders across the entertainment ecosystem, from producers seeking to align their projects with audience expectations to platforms refining their recommendation algorithms. Through intuitive visualizations and data-driven observations, this report aspires to deepen understanding of what makes movies resonate with audiences while offering a lens into the dynamic forces shaping the industry.

== The Data 

=== Datasets

The four raw datasets selected for the study, all from Kaggle, were used to analyze movie data and provide personalized recommendations and industry trend predictions from macro movie data, user ratings, and movie-specific information, respectively. After organizing and cleaning the original datasets, they are merged into two .csv datasets for subsequent visual analysis of the movie industry.

- *The Movie Dataset*: The dataset comprises metadata for all 45,000 movies included in the Full MovieLens Dataset, which encompasses movies released on or before July 2017. The dataset includes information on the cast, crew, plot, keywords, budget, revenue, posters, release dates, languages, production companies, countries, TMDB vote counts and vote averages. Additionally, it contains files with 26 million ratings from 270,000 users for all 45,000 movies, with ratings on a scale of 1-5 obtained from the official GroupLens website.
- *Top 1000 Highest Grossing Movies:* The dataset comprises information about the 1,000 highest-grossing films produced by Hollywood studios. It has been updated to reflect the most recent data as of 25 September 2023. The data has been collated from a range of sources, including the Internet Movie Database (IMDb), Rotten Tomatoes and other similar platforms, and has been aggregated for the purpose of performing various data operations.
- *Movie Dataset: Budgets, Genres, Insights:* The movies dataset is a comprehensive collection of information about 4,803 movies. It provides a wide range of details, sourced from #link("github.com/"), about each film, including budget, genres, production companies, release date, revenue, runtime, language, popularity, and more.
- *IMDB 5000 Movie Dataset:* The dataset comprises detailed information about over 5,000 films sourced from the Internet Movie Database (IMDb). It encompasses a range of data points, including the cast, keywords, reviews, budgets, and other pertinent information. Of particular note is the inclusion of data from the cast's Facebook pages and associated data.

=== Data Integration Strategy

Since the above datasets provide rich information in different dimensions respectively, this study needs to organize and merge these datasets to create a comprehensive data framework covering multiple dimensions such as basic information, ratings, box office, genres, production companies, and so on, to support a wide range of analytical needs.

For the specific steps of integration, data cleansing is first required to remove duplicates, fill in missing values, and standardize the content format, followed by merging and de-duplicating the data tables based on the movie title and IMDb ID fields as key fields. Integrating multiple datasets allows for in-depth analysis across multiple dimensions of movie industry-specific information, and is more conducive to exploring the relationship between production budgets and box office revenues.

The processed dataset is divided into the following two, focusing on macro-level information and movie-specific details, respectively. The larger dataset mainly contains basic information such as movie title, release date, duration and other basic information and production information such as movie ratings and box office budget, as well as its social media situation outlining the popularity and specific performance of the movie. This data is mainly used to analyze the overall trend of the movie industry from a macro point of view, to explore the specific performance of movies in different periods and genres, and to better understand the industry development trend and user preferences. The other data is smaller and expands on the previous dataset with information on specific box office situations, distribution companies and main actors, to more deeply analyze the impact of specific characteristics of a movie on its box office and ratings.

= Tasks

This study divides the visual analysis about the movie industry into the following five sections, which analyze the movie industry in terms of information such as the overall trend of the movie industry, changes in capital investment, and key factors affecting the box office and ratings of movies.

== General Overview of Movies

=== Introduction

The global film industry is vast and diverse, encompassing movies from different genres, production scales, and cultural backgrounds. To better understand the overall structure and patterns of this industry, it is crucial to first gain a comprehensive overview of the dataset. This section aims to provide insights into the foundational aspects of the movie dataset, such as the total number of films, their distribution over time, and the diversity in genres and production origins through different visualizations.

=== Number of Movies

We use a bar chart to illustrate the number of movies each year and its trend. The x-axis represents the year and the y-axis represents the number of movies. It can be seen that the number of movies increased steadily before the 21st century, and that the increase became significantly larger after the 21st century.

#figure(
  image("images/number_of_movies_by_year.png"),
  caption: [Number of Movies by Year]
)

Before 21st century, the movie production is quite expensive and complicated. These limitations make it hard to produce movies, resulting the slow increase. However, when it comes to the 21st century, advances in digital filmmaking, globalization of cinema, the rise of streaming platforms, and increased accessibility significantly boosted production. Emerging markets and government incentives also played a role.

Additionally, we have designed this chart to be interactive. Users can select a specific year to view the details of the overall movie statistics for that year in the following charts.

Meanwhile, the table below shows the number of movies produced by different regions. The table shows the top 20 countries in terms of the number of movies produced. The United States produced the most movies (18,429), followed by the United Kingdom (3,072) and France (2,711). It is worth noting that many movies are produced by multinational joint ventures, and here we take the first field. While this allows for a simplification of data organization, it also creates some bias in our analysis.

#figure(
  image("images/number_of_movies_by_region.png", width: 100pt),
  caption: [Number of Movies by Region]
)

=== Movie Genres

A tree map is employed to demonstrate the distribution of movie genres. There are possibly multiple genres for a movie, and we choose the first genre tag as the main genre of the movies. The size and the color depth represent the proportion of the genre.

#figure(
  image("images/distribution_of_movie_genres.png", width: 400pt),
  caption: [Distribution of Movie Genres]
)

And here is a bar chart illustrating the popularity of different movie genres. Drama and comedy are not only the most popular genres but also the most produced genres, reflecting their broad appeal and frequent production in the film industry. Action follows closely, driven by its high entertainment value and ability to attract a diverse audience. Genres such as horror, adventure, and thriller show moderate popularity and a relatively small production scale, appealing to more niche but dedicated audience groups. On the other hand, genres like music, western, and mystery are the least popular, likely due to their narrower audience reach or lower production volume. Overall, the charts highlight the dominance of versatile genres while showcasing the varied preferences of movie audiences.

#figure(
  image("images/popularity_by_genre.png", width: 350pt),
  caption: [Popularity by Genre]
)

However, focusing on the first genre tag may overlook the impact of hybrid genres while simplifying the analysis. Therefore, it is important to conduct further data mining and in-depth visualization.

=== Movie Production Companies

@Movie_Company(a) illustrates the popularity of various film production companies through circles of differing sizes, where larger circles indicate higher popularity. Cherin Entertainment emerges as the most prominent company, significantly overshadowing its competitors and suggesting a strong influence in the industry. Newgrange Pictures, CoMix Wave Films, and 1492 Pictures are notable mid-tier players, demonstrating solid reputations without reaching Cherin's level of prominence. The diversity of companies, ranging from well-known entities like Twentieth Century Fox to smaller firms such as Pandemonium, highlights the variety within the film sector.

@Movie_Company(b) depicts the number of movies produced by various film companies, represented through circles of varying sizes. Each circle's size corresponds to the total number of films released by the company, providing a visual representation of their output. Companies such as Warner Bros. and Walt Disney Pictures dominate in terms of film production volume, suggesting a robust capacity for creating content. However, the average popularity of the films produced by these companies may vary significantly. For instance, while Warner Bros. has a large output, the average popularity of its films might be influenced by factors such as genre diversity and marketing strategies. Conversely, companies like Universal Pictures and Twentieth Century Fox, with fewer films, may have a higher average popularity per movie, indicating a focus on quality or blockbuster hits. 

#figure(
  grid(
    columns: (auto, auto),
    [
      #align(left)[(a)]
      #image("images/popularity_by_company.png")
    ],
    [
      #align(left)[(b)]
      #image("images/number_of_movies_by_company.png")
    ]
  ),
  caption: [Movie Companies]
)<Movie_Company>

This analysis highlights the relationship between production volume and average film popularity, suggesting that both quantity and quality play crucial roles in a company's overall success in the film industry.

== Trends of the Movie Industry

=== Introduction

The movie industry has experienced profound shifts in its financial landscape, characterized by changes in funding, production costs, and box office revenues. This section delves into the evolving dynamics of financial investment and returns within the industry. By analyzing the relationship between investment and output, we aim to shed light on the flow of capital and return trends. This exploration will provide a deeper understanding of how financial strategies impact the production and success of films, offering valuable insights into the monetary mechanisms that drive the industry forward.

=== Movie Industry Development

The chart illustrates the trends in budget and revenue in the movie industry from 1925 to 2020. In the early years, both budget and revenue remained low and stable, reflecting modest investment and returns in the mid-20th century. During the 1980s and 1990s, there was a gradual increase, indicating expanded production scales and market growth. The 2000s and 2010s saw significant spikes, highlighting the impact of blockbuster films and technological advancements, leading to substantial financial investments and higher box office returns. However, from the 2010s to 2020, there were fluctuations despite the high levels of budget and revenue, possibly due to changing audience preferences and the rise of digital streaming platforms. Overall, the chart demonstrates a strong correlation between increasing budgets and rising revenues, underscoring the growing financial investments and returns in the movie industry over time.

#figure(
  image("images/movies_industry_development.png", width: 400pt),
  caption: [Movie Industry Development]
)

=== Budget and Revenue

@fig:budget_revenue(a) illustrates the distribution of movie budgets and revenues across different years. Each rectangle represents a year, with the larger and the darker of the rectangle indicating a higher level of budget and revenue. The larger and darker blocks, particularly in the 2000s and 2010s, reflect a period of increased spending and higher box office returns, while lighter and smaller blocks in earlier years depict lower financial activity. This visualization effectively highlights the growth in financial scale within the movie industry over time.

@fig:budget_revenue(b) illustrates the relationship between movie budgets and box office revenues. Each point represents a film, with the x-axis showing the budget and the y-axis indicating the revenue. The plot reveals a general trend where higher budgets can lead to higher revenues, but there is considerable variability. Some films achieve substantial revenue with moderate budgets, while others with large budgets do not perform as well. This indicates that while budget is a factor in box office success, it's not the sole determinant.

#figure(
  grid(
    columns: (auto, auto),
    column-gutter: 5pt,
    [
      #align(left)[(a)]
      #image("images/budget_and_revenue.png")
    ],
    [
      #align(left)[(b)]
      #image("images/scatter_budget_reveune.png")
    ]
  ),
  caption: [Budget and Revenue]
)<fig:budget_revenue>

Users can interact with the treemap through clicking on different years, which then links to three additional detailed charts. These charts provide an in-depth look at the geographic distribution of movie budgets and revenues for the selected year. This functionality enables a deeper exploration of how financial resources were allocated and revenue was generated across different regions, offering valuable insights into the global dynamics of the film industry for that specific year.

=== Company and Revenue

The pie chart displays the revenue distribution among different movie production companies, with each segment representing a company's share of total income. Different colors distinguish the contributions of each company. Major players like Walt Disney Pictures, Universal Pictures, and others are prominent, indicating their significant roles in revenue generation within the industry. This visualization effectively highlights the competitive landscape and dominance of certain studios in the movie market.

#figure(
  image("images/companies_and_revenue.png", width: 400pt),
  caption: [Companies and Revenue]
)

=== Geographical Distribution of Budget and Revenue

The two maps depict the distribution of movie budgets and box office revenues across various countries and regions. Darker shades on the maps indicate higher values. The United States stands out with the deepest colors, reflecting its significant contribution to both budgets and revenues in the film industry. Other regions show varying levels of financial activity, highlighting the global nature of movie production and revenue generation. These visualizations effectively demonstrate the geographical disparities in the film industry's financial landscape.

#figure(
  grid(
    columns: (auto, auto),
    column-gutter: 5pt,
    [
      #image("images/budget_country.png")
    ],
    [
      #image("images/reveune_country.png")
    ]
  ),
  caption: [Geographical Distribution of Budget and Revenue]
)

=== Summary

This part is a continuation of the overview section. A combination of various charts is used to comprehensively explore the changes in the development of the movie industry and to deeply analyze the dynamic relationship between capital investment and box office output. This helps users better understand the economic trends of the movie industry. Users can further deepen their understanding of the financial flows of the movie industry by selecting different years through the interactive function to view the data performance of a specific year.

== Factors Affecting Movie Box Office

=== Introduction

Understanding the factors that influence movie box office performance is crucial for stakeholders in the film industry. This section explores key elements such as marketing strategies, star power, genre preferences, release timing, and critical reviews. By analyzing these factors, we aim to provide insights into how they contribute to a film's financial success, helping filmmakers and producers make informed decisions to maximize box office returns.

=== Gross of Movies Published Each Year

The bar chart illustrates the total gross of films released each year from 1925 to 2020. It shows a significant upward trend, particularly from the late 1970s onwards, with noticeable peaks in the 2000s and 2010s. This increase reflects the growing scale and financial impact of the film industry over time. The darker shades in recent years indicate higher gross values, highlighting the era of blockbuster films and expanded global distribution. This visualization effectively captures the industry's growth in revenue generation across decades.

#figure(
  image("images/gross_of_films_each_year.png", width: 400pt),
  caption: [Gross of Movies Published Each Year]
)

=== Different Genres

The bubble chart displays the gross revenue of films across different genres. Each bubble's size represents the total earnings for that genre. Action films dominate with the largest bubble, followed by Comedy and Adventure, indicating their strong box office performance. Drama, while smaller, also contributes significantly to revenue. Other genres like Crime, Horror, and Animation show varied but notable earnings. This visualization highlights the popularity and financial success of different film genres in the industry.

#figure(
  image("images/gross_with_different_genre.png", width: 300pt),
  caption: [Gross with Different Genres]
)

=== Sum of Fans

@scatter_point_gross (a) depicts the relationship between a movie's gross revenue and the sum of fans, measured by actor Facebook likes. Each point represents a film, with the x-axis showing the sum of fans and the y-axis indicating the gross revenue. There is a general upward trend, suggesting that films associated with actors who have larger fan bases tend to earn higher revenues. However, there is considerable variability, indicating that while fan base size can influence box office success, it is not the sole factor.

=== Budget

@scatter_point_gross (b) shows the relationship between a movie's budget and its gross revenue. Each point represents a film, with the x-axis indicating the budget and the y-axis showing the gross revenue. There is a positive correlation, suggesting that higher budgets often lead to higher revenues. However, there is considerable spread, indicating that while a larger budget can contribute to box office success, it is not the sole determinant.

=== Aspect Ratio

@scatter_point_gross (c) illustrates the relationship between a movie's aspect ratio and its gross revenue. Each point represents a film, with the x-axis showing the aspect ratio and the y-axis indicating the gross revenue. The data suggests that most films cluster around common aspect ratios, with no clear correlation between aspect ratio and box office success. While some films with typical aspect ratios achieve high revenues, this factor alone does not appear to significantly influence gross earnings.

#figure(
  grid(
    columns: (auto, auto, auto),
    rows: (auto),
    row-gutter: 1em,
    column-gutter: 1em,
    [ #align(left)[(a)]
      #image("images/gross_fans.png", width: 150pt)
    ],
    [
      #align(left)[(b)]
      #image("images/gross_budget.png", width: 150pt)
    ],
    [
      #align(left)[(c)]
      #image("images/gross_aspect.png", width: 150pt)
    ],
  ),
  caption: [Gross vs. Sum of Fans, Budget and Aspect Ratio]
)<scatter_point_gross>

=== Countries 

The map shows the gross revenue of films across different countries. The shades of blue indicate the level of gross earnings, with darker shades representing higher revenues. The United States, Canada, and several European countries display significant earnings, highlighting their substantial contributions to global box office revenues. This visualization effectively illustrates the geographic distribution of film industry success, emphasizing key markets worldwide.

#figure(
  image("images/gross_country.png"),
  caption: [Gross in Different Countries]
)

=== Directors

The treemap displays the box office gross of the top ten directors. Each rectangle represents a director, with larger areas indicating higher gross earnings. This visualization highlights which directors have achieved the most financial success in terms of box office revenue, providing a clear comparison of their impact in the industry.

=== Main Actor
    
The treemap shows the box office gross of films starring the top ten actors. Each rectangle represents an actor, with larger areas indicating higher gross earnings. This visualization highlights which actors have led the most financially successful films, providing a clear comparison of their impact in the industry.    

For more detailed information, we provide such things as country, movie title, language and box office receipts in a tabular format.

=== Highlights

- The charts cover global box office data, a wide range of movie genres, and the performance of different directors and lead actors, providing a comprehensive view to analyze the movie market.
- A variety of visualization formats such as maps, circle charts and tree diagrams are used to make the data more intuitive and easy to understand. The use of different colors and sizes effectively distinguishes different levels of box office revenue.
- Users can view data in different dimensions by selecting different categories (e.g. director, lead actor), which improves the flexibility and depth of data analysis.

To sum up, this part shows the box office revenue trends and influencing factors of the movie industry through multi-faceted data, providing strong support for analysis and decision-making.

== Factors Affecting Movie’s IMDb Ratings

=== Introduction

IMDb ratings are a widely recognized metric for gauging audience sentiment and critical reception, making them a valuable indicator of a movie's quality and appeal. This section explores the factors that influence these ratings, aiming to uncover the underlying patterns and correlations that contribute to high or low audience scores. By analyzing key attributes such as release year, budget, runtime, and director popularity, we aim to identify trends and characteristics shared by highly rated films.

Through detailed visualizations, this analysis not only highlights the elements that resonate most with audiences but also offers insights into how these factors interplay to shape overall perceptions. By understanding these dynamics, we provide actionable insights for filmmakers, distributors, and platforms to align their strategies with audience preferences and expectations.

In this specific part, we divide the factors which influence the IMDb rating into 4 parts, including budget, content rating, region and era.

=== IMDb Rating vs. Budget
    
A scatter graph is employed to explore the relationship between a movie’s budget and its IMDb rating. This analysis aims to identify whether higher production budgets consistently correlate with better audience reception or if low-budget films occasionally achieve critical acclaim.
        
From the chart above, it is easy to see that movies with low IMDb ratings tend to have rather low budgets, while movies with relatively high budgets (e.g. over \$180,000,000) can achieve at least a moderate rating (e.g. over 5.0).
    
We can also see that movies with quite high IMDb ratings (e.g. *The Godfather, Fight Club*) have quite low budgets compared to others. At the same time, movies with a super high budge, for example, *Pirates of the Caribbean: On Stranger Tides*, have an unsatisfactory rating, which may not correspond to their budget.
    
We have the following conjectures about this phenomenon:
    
1. *High-budget movies often prioritize commercial success over artistic value*
  - *Different target audiences*: High-budget films are typically aimed at a broader audience, focusing on special effects, action sequences, and star power. These elements may not always meet audience expectations for deep storytelling or innovation.
  - *Safe strategies*: To ensure a return on investment, high-budget movies often follow proven formulas, remakes, or sequels, which can result in a lack of originality and lower audience ratings.
2. *Low-budget movies tend to focus more on content and creativity*
  - *Greater creative freedom*: Low-budget films may allow directors more room for experimentation with themes and expression, attracting audiences who value artistic quality and compelling narratives.
  - *Word-of-mouth effect*: High-rated, low-budget films often rely on word-of-mouth promotion. Their evaluations are more likely to reflect the quality of the story and emotional resonance rather than visual spectacle.
3. *Audience expectation management*
  - *High expectations from big budgets*: Viewers generally have higher expectations for high-budget films. If the movie fails to meet those expectations, the ratings might suffer.
  - *The "pleasant surprise" effect of low budgets*: Audiences tend to have lower expectations for low-budget films. When these movies exceed expectations, they are more likely to receive high ratings.
4. *Bias in rating samples*
  - *Difference in audience size*: High-budget films attract a more diverse audience, leading to greater variability in ratings. In contrast, low-budget films tend to appeal to niche audiences, resulting in more consistent ratings.
  - *Subjective preferences of reviewers*: Film critics and avid moviegoers often appreciate the creativity and narrative depth of low-budget films, while being more critical of "blockbuster" movies.
5. *Trade-offs in resource allocation*
  - *Overinvestment in visual effects*: High-budget films may allocate a significant portion of resources to technical aspects (e.g., CGI, set design), potentially neglecting script quality and character development, which can lead to lower audience ratings.
  - *Attention to detail in low-budget films*: Budget constraints force creators to focus on storytelling and character development, which can enhance the overall quality of the film.

=== IMDb Rating vs. Regions
    
Utilizing a map chart, this topic examines the geographical diversity of movie production by visualizing the average IMDb ratings of films from different regions. The analysis highlights regional trends, uncovering cultural or industry-specific factors that may impact audience ratings.
        
The map above illustrates the average ratings of movies in different regions. We can see that the regions that we don't think produce great films can have a fairly high average rating, while the distribution of ratings in the United States is more similar to the overall distribution of global film ratings.
    
We can draw these conclusions about this phenomenon: 
    
1. *The Global Influence of Hollywood*
        - **Wide audience reach**: Hollywood, as the epicenter of the global film industry, produces movies that cater to a vast and diverse audience. Its films dominate the global box office and are widely accessible, making them a substantial part of the global dataset.
        - **Cultural export**: U.S. films are heavily marketed and distributed worldwide, shaping the tastes and expectations of international audiences. As a result, global rating patterns naturally align with those of U.S. films.
    2. **Diversity in Genre and Style**
        - **Broad spectrum of films**: The U.S. produces a high volume of films spanning nearly every genre, style, and audience demographic. This diversity ensures that the rating distribution of U.S. films reflects a wide range of audience preferences, similar to the global dataset.
        - **Catering to international markets**: Many U.S. productions are designed to appeal to global audiences, further aligning their reception with worldwide trends.
    3. **Volume and Accessibility of U.S. Films**
        - **Overrepresentation in global data**: Due to the sheer volume of films produced in the U.S. and their accessibility on international platforms, these films constitute a significant portion of movies rated on IMDb. Their influence skews global rating trends toward the patterns seen in U.S. films.
        - **Exposure bias**: As U.S. films dominate streaming services, cinemas, and international markets, global audiences are more likely to watch and rate them, reinforcing the similarity in rating distributions.
    4. **Audience and Rating Behavior**
        - **Diverse audience base**: Just as U.S. films attract a global viewership, the audiences rating these films on IMDb come from diverse cultural and demographic backgrounds. This contributes to a balanced distribution that mirrors global patterns.
        - **Wide appeal vs. niche markets**: Unlike films from smaller regions that may cater to specific cultural or artistic tastes, U.S. films aim for broad appeal. This inclusivity results in ratings that better represent global averages.
    5. **Contrast with Films from Other Regions**
        - **Selective exposure of non-U.S. films**: As mentioned earlier, films from non-dominant regions often achieve higher ratings due to their selective international exposure and appeal to niche audiences. This creates a disparity between their rating patterns and those of U.S. films, which are subject to a broader range of criticism and viewer expectations.
        - **Normalization of U.S. film ratings**: The large dataset of U.S. films, combined with a wider spectrum of audience reception, produces a normalized rating distribution that closely aligns with global patterns.
- **IMDb Rating vs. Content Rating**
    
    Bar charts are used to showcase the average IMDb ratings of films categorized by their content ratings (e.g., G, PG, R). This comparison helps identify which content categories resonate most with audiences and whether content restrictions influence viewer perceptions.
    
    ![image.png](https://prod-files-secure.s3.us-west-2.amazonaws.com/81fefee1-6498-418a-b5a0-defeb8e7d8e3/59d5f3be-75f6-4e96-b6b1-679b08f9a2d5/c812bc3e-3cc3-4821-a6ef-ec5c240e32ab.png)
    
    ![image.png](https://prod-files-secure.s3.us-west-2.amazonaws.com/81fefee1-6498-418a-b5a0-defeb8e7d8e3/d935bec1-fd0e-47ad-bde5-b69ec44fdaf2/1f4a67ad-3d28-4acd-b2b9-7c170b3a6750.png)
    
    The chart shows that PG-13-rated movies have the highest film count, indicating their dominance in the movie industry. This is likely because PG-13 films target a broad audience, including teenagers and adults, making them highly marketable. R-rated films have a substantial count, reflecting their popularity among adult audiences, while PG-rated films are also significant, appealing to family audiences. The count of G-rated (General Audiences) and X-rated (Adults Only) films is very low, suggesting that these categories are either less commonly produced or face limited market demand.  
    
    Despite their low count, X-rated films achieve the highest average IMDb ratings. This aligns with their niche audience appeal and selective exposure, as discussed earlier. These films are often rated by viewers who appreciate their specialized content, resulting in higher scores. G-rated films achieve the second-highest ratings, reflecting their wholesome, family-friendly content that resonates well with audiences. These films may also benefit from less critical scrutiny. Despite their high production volume, PG-13 films exhibit the lowest average IMDb ratings, likely due to their focus on mass-market appeal, which can lead to diluted quality or overexposure to criticism. R-rated films, targeted toward adult audiences with mature themes, achieve moderately high ratings, while PG-rated films, catering to younger audiences, show slightly higher ratings than PG-13.
    
    We can obtain follow key observations: 
    
    - **Inverse relationship between quantity and quality**: The PG-13 category dominates in terms of count but performs the worst in average IMDb ratings, suggesting that producing more films in this category does not guarantee higher quality or audience satisfaction.
    - **Specialized content stands out**: Both X-rated and G-rated films, while low in quantity, achieve the highest ratings, reinforcing the idea that focused or niche content tends to resonate better with their intended audiences.
    
    These phenomena can be explained by the following factors: 
    
    - **Market targeting**: Studios might produce a high volume of PG-13 films due to their marketability, but this analysis highlights the need to balance quantity with quality to achieve better audience reception.
    - **Niche opportunities**: The high ratings of X-rated and G-rated films suggest opportunities for filmmakers to explore niche genres or family-oriented content for impactful results.
    - **Audience expectations**: PG-13 films must innovate to meet the diverse expectations of a broad audience, as their current formulaic approach seems to underperform compared to other categories.
- **IMDb Rating vs. Era**
    
    By employing bar and pie charts, this analysis investigates IMDb ratings across different eras, revealing trends in audience reception over time. Additionally, the proportion of highly rated films (ratings above 8.0) in each era is examined to understand the evolution of critically acclaimed filmmaking.
    
    ![image.png](https://prod-files-secure.s3.us-west-2.amazonaws.com/81fefee1-6498-418a-b5a0-defeb8e7d8e3/cfc22c02-2396-4aa3-b091-0de56157fcfe/image.png)
    
    From the chart, we can obtain following information: 
    
    - **1950 and earlier have the highest average rating (7.475):** Movies produced in this era demonstrate the highest average IMDb ratings. This suggests that earlier films are held in high regard, potentially due to their historical significance, artistic innovation, or the enduring impact of classic storytelling.
    - **1950-1975 maintains relatively high ratings:** This era also has above-average ratings, though slightly lower than the pre-1950s. This period corresponds to the "Golden Age of Hollywood" and other global cinematic movements, characterized by high-quality filmmaking and iconic directors.
    - **1975-2000 sees a noticeable drop in ratings:** Movies from this era show a significant decline in average ratings. This could be attributed to an increase in the volume of films produced, resulting in a wider spectrum of quality, or shifts in audience preferences as the industry moved toward blockbuster-driven models.
    - **Post-2000 era’s average rating is the lowest among these eras:** The most recent period still falls below the historical average, indicating that modern films may not yet achieve the same critical acclaim as older classics. This might be due to oversaturation in the industry or a shift toward commercialism.
    
    Here are some possible explanations for trends: 
    
    - **Nostalgia and Historical Significance:** Older films, especially those from 1950 or earlier, may benefit from nostalgic bias and their role as pioneers in cinema. Viewers and critics often hold these films in higher regard due to their cultural and historical value.
    - **Changes in Production Models:** As the film industry grew in the 1975-2000 period, the focus shifted toward blockbuster franchises and commercial appeal, potentially leading to a dilution of quality. This change in focus might explain the dip in average ratings.
    - **Impact of Modern Audience Expectations:** Post-2000 films face more diverse and critical audiences with higher expectations, particularly due to the ease of access to films globally. Modern audiences often compare films across a broader spectrum, leading to more polarized ratings.

== Analysis of the Relationship between High Ratings and High Box Office

=== Introduction

The relationship between high ratings and box office success is a key focus for the film industry. This analysis explores how critical acclaim and audience approval correlate with financial performance. By examining data on film ratings and box office earnings, we aim to uncover patterns that indicate whether high ratings consistently lead to higher revenues. Understanding this relationship can provide valuable insights for filmmakers and marketers seeking to optimize both the artistic and commercial success of their films.

=== Visualization and Analysis

- **Gross Distribution**
    
    The provided visualization represents the distribution of box office revenue across a range of movies. A significant 75.43% of the total box office revenue comes from films that earned less than 100 million dollars, as shown by the dominant bar on the left side of the graph. Beyond this range, revenue contributions drop sharply, with only 9.86% coming from the next group of films. The distribution follows a long-tail pattern, where a small number of blockbuster films generate extremely high revenue, but the majority of movies earn significantly less. This suggests that while a few high-grossing films attract attention, the bulk of the industry's overall performance is driven by a large number of lower-grossing films. Therefore, understanding and optimizing the success of these lower-revenue films could be crucial for sustaining the overall profitability of the movie industry.
    
    ![Gross Distribution.png](https://prod-files-secure.s3.us-west-2.amazonaws.com/81fefee1-6498-418a-b5a0-defeb8e7d8e3/551c3051-c497-47fb-9922-b75f284a6902/Gross_Distribution.png)
    
- **Rating Distribution**
    
    The bar chart displays the overall distribution of movie ratings, with the horizontal axis representing the rating scores and the vertical axis showing the percentage distribution of these ratings. The data reveals that over 90% of movies have ratings between 4.5 and 8.0, indicating that most films fall within the range of medium to relatively high scores. The peak of the distribution occurs between 6.0 and 6.5, where 27.77% of the movies are clustered. This suggests that while there are relatively few extremely low or extremely high-rated films, the majority of movies receive moderate evaluations from viewers, with a concentration around the 6 to 7 rating range.
    
    ![Rating Distribution.png](https://prod-files-secure.s3.us-west-2.amazonaws.com/81fefee1-6498-418a-b5a0-defeb8e7d8e3/de64c0e0-197f-4ad4-9e41-c989ad0caf85/Rating_Distribution.png)
    
- **The relationship between Gross and Rating**
    
    This scatter plot explores the relationship between movie box office revenue and ratings. The horizontal axis represents the average rating, while the vertical axis represents the box office revenue. A trend line is included in the chart, showing a generally positive correlation between the two variables. This suggests that movies with higher ratings tend to have higher box office earnings. There are, however, two significant outliers: *Avatar* and *Star Wars: The Force Awakens*, both of which had exceptionally high grosses compared to other films, despite not having the highest ratings. These two outliers warrant separate analysis, as their success may be due to factors beyond just ratings, such as franchise popularity or large fan bases. Overall, while higher ratings are generally associated with higher revenue, blockbuster films like these can achieve extraordinary box office success regardless of their specific ratings.
    
    ![the_relationship_between_gross_and_rating.png](https://prod-files-secure.s3.us-west-2.amazonaws.com/81fefee1-6498-418a-b5a0-defeb8e7d8e3/057b37ae-b3c1-4d24-9fc1-701d43b1e1a5/the_relationship_between_gross_and_rating.png)
    
- **Genres of highly rated and high-grossing films**
    
    This pie chart presents the distribution of genres among 22 highly rated (with ratings above 8.0) and high-grossing (box office above 100 million) films. The data reveals that *Drama* (31.82%) and *Adventure* (22.73%) are the genres most likely to achieve both high ratings and strong box office performance. Other notable genres include *Comedy* (9.09%) and *Romance* (4.55%), though they are less dominant. This indicates that films in the Drama and Adventure genres tend to appeal to both critics and audiences, making them more likely to achieve success in both ratings and revenue.
    
    ![genres_of_highly_rated_and_high_grossing_films.png](https://prod-files-secure.s3.us-west-2.amazonaws.com/81fefee1-6498-418a-b5a0-defeb8e7d8e3/841f7591-c9b6-45ba-860e-f8ed8582309c/genres_of_highly_rated_and_high_grossing_films.png)
    
- Countries of highly rated and high-grossing films
    
    This map illustrates the countries where highly rated (ratings above 8.0) and high-grossing (box office above 100 million) films were produced. The data shows that the majority of these films come from the United States, which dominates the global film industry. Europe, particularly countries like the United Kingdom and France, also contributes a notable portion. This distribution highlights the strong global influence of Western cinema, particularly from the U.S. and Europe, suggesting that Western culture continues to be highly popular and influential worldwide in terms of both critical acclaim and box office success.
    
    ![countries_of_highly_rated_and_high_grossing_films.png](https://prod-files-secure.s3.us-west-2.amazonaws.com/81fefee1-6498-418a-b5a0-defeb8e7d8e3/fc42ee21-c63f-4016-a0cb-68cc5faa7a59/countries_of_highly_rated_and_high_grossing_films.png)
    

=== Summary

The analysis of the relationship between movie box office and ratings reveals several key insights. 

1. First, box office revenue is unevenly distributed, with most films earning relatively low revenue and only a few achieving high box office success. Ratings, on the other hand, are concentrated between 4.5 and 8.0, indicating that while most films are of decent quality, truly outstanding ones are limited. There is a positive correlation between ratings and box office revenue, suggesting that higher-rated films tend to perform better financially. 
2. Genre analysis shows that *Drama* and *Adventure* films are the most likely to achieve both critical and commercial success, making them valuable focuses for future film production. 
3. In terms of geography, movies from the United States and Europe dominate among high-grossing and highly rated films, highlighting the significant influence of Western culture in the global film industry. 

These findings provide useful guidance for filmmakers and distributors aiming to optimize both critical reception and box office performance.

= Summary and Analysis

== Advantages of the visualization approach

For the analysis of the movie industry, the Tableau tool was selected for this study to perform a multi-dimensional visualization, choosing a number of different types of charts and graphs to reveal overall trends and key factors in the film industry. The following section analyzes the advantages of these specific visualization methods and explains why these chart formats are particularly effective when analyzing film data.

1. Line Chart
    - Use Scenario: Used to show annual trends in movie numbers, budgets and revenues.
    - Advantages:
        - Trend analysis: line charts are well suited for presenting time-series data and can clearly reflect trends in the data. In the analysis of movie numbers and box office revenues, line charts help observe the rapid growth of movie production and investment after the 21st century.
        - Identify inflection points: It can visually identify key time points, such as unusual peaks or troughs in movie production or box office in a particular year.
        - Multiple Line Comparison: In the analysis of budget and box office revenue, line charts can show multiple data lines at the same time, making it easy to compare the trends of different data items and reveal the relationship between budget and box office.
2. Tree map
    - Usage Scenario: Analyze the distribution of movie genres, box office performance of different directors or lead actors.
    - Advantages:
        - Hierarchical Structure and Proportion Display: The tree diagram can display the hierarchical structure and proportion of the data at the same time. When used to analyze the distribution of movie genres, the proportions of different types of movies can be clearly seen, such as the largest proportion of drama and comedy movies.
        - Efficient use of space: Compared with bar charts and pie charts, tree charts utilize space more efficiently and are suitable for displaying a large number of categories of data, especially when the data has more dimensions and needs to be compared.
        - Combination of color shades and area size: The ability to express both the number of movie genres and their popularity (e.g., box office revenues) through color shades and rectangular area size allows users to see at a glance the differences in the performance of movies in different categories.
3. Bubble Chart
    - Usage Scenario: Analyze the number of production, popularity and box office revenue of different types of movies produced by movie studios.
    - Advantages:
        - Multi-dimensional display: Bubble Chart displays data in multiple dimensions at the same time through bubble size, position and color, such as the number of production and popularity of movie studios, which can visualize the comparison between different companies.
        - Strong visual impact: When analyzing the popularity of movie companies, the bubble chart is able to show high-income companies through large bubbles and low-income companies through small bubbles, which has a strong visual impact and is easy to attract users' attention.
        - Suitable for displaying distribution and concentration: It can help to identify concentration trends and outliers in the data, for example, certain companies have a high number of movies but not a high popularity, or certain companies have a low number of movies but a good performance at the box office.
4. Scatter Plot
    - Usage Scenario: used to analyze the relationship between budget and box office receipts, budget and IMDb rating.
    - Advantages:
        - Show data correlation: Scatter plots are the best choice for analyzing the relationship between two sets of numerical data. With a scatterplot, you can see the positive correlation that exists between budget and box office revenue, revealing that high-budget movies usually perform better at the box office.
        - Identify outliers: Scatterplot can effectively identify outliers, such as high-budget but poorly rated movies, which may suggest special circumstances or problems in the movie market.
        - Suitable for analyzing large data sets: Scatterplot can display a large number of data points on a single plot, making it easy to observe the overall distribution and trends in the data set.
5. Map Visualization
    - Usage Scenario: Show movie production, box office revenue and IMDb ratings for each country around the world.
    - Advantages:
        - Spatial data analysis: Map visualization visualizes geographic distribution characteristics and is ideal for analyzing the performance of the film market on a global scale. Users can visualize countries with higher box office revenues, such as the United States and China, through color shades.
        - Quickly Identify Regional Differences: The display of geographic information can help users quickly identify differences in film market performance across regions. For example, the rise of certain emerging markets (e.g. China) or the dominance of traditional movie powers (e.g. the US).
        - Enhanced User Experience: The map visualization is highly interactive, allowing users to click on different countries to view detailed information and increase user engagement.
6. Interactive Visualization
    - Usage Scenario: Linkage analysis between multiple charts, e.g. filtering the corresponding data display according to year, type or company changes.
    - Advantages:
        - Enhance analysis efficiency: The interactive feature enables users to filter by specific dimensions (e.g., year, movie genre) to quickly locate and analyze data of interest.
        - Dynamic Exploration of Data: By clicking on a specific genre or year, users can dynamically view the changes in the relevant data and dig deeper into the trends and reasons behind the data.
        - Personalized Analysis: Interactive visualization allows users to adjust the filtering criteria according to their needs for personalized in-depth analysis, enhancing the flexibility of data exploration.

Overall, Tableau, as a powerful data visualization tool that combines a variety of chart forms (line charts, tree charts, bubble charts, scatter plots, maps, etc.), demonstrates the following advantages when analyzing film industry data:

- Multi-dimensional display: Supports the visualization of different data types, capable of displaying numerical, sub-typed, time-series and geographic data at the same time to meet the needs of multi-dimensional analysis.
- Efficient and intuitive: Through the combination of colors, sizes, shapes and other visual elements, it makes the trends and outliers of the data clear at a glance, which effectively improves the efficiency of data analysis.
- Strong Interactivity: Supporting linkage between charts and dynamic filtering functions, users can adjust filtering conditions in real time according to their needs for personalized analysis and improve the depth of data exploration.

The combination of these chart forms not only enhances the comprehensiveness and meticulousness of the analysis, but also helps users to deeply understand the various trends and influencing factors of the film industry through an intuitive and clear visual display, providing strong support for decision-making.

== Other visualization methods

1. Box Plot
    - Focus on distributional characteristics rather than trend analysis: box plots are mainly used to analyze the distribution of data, outliers and interquartile range. Although it can show the degree of data dispersion, the trend analysis of the time series, the change rule display is more limited.
    - Not intuitive: For users with non-data analysis background, box plots have a higher threshold of understanding and are not as intuitive as line graphs. Especially when analyzing time series trends (e.g. changes in box office revenues), line graphs can clearly present growth and decline trends, which are easier to be understood by users.
2. Bar Chart
    - Underutilized space: When displaying a large number of categories (e.g., movie genres, production companies), bar charts can be crowded due to too many columns and horizontal contrast is not as clear as tree charts. Tree Charts can show more information in a limited space and the hierarchical structure allows viewers to see both overall and subdivided categories.
    - Trends and Changes are Difficult to Present: Bar charts are unable to consistently show changes in trends when presenting time-series data. In contrast, Horizontal Charts have more obvious advantages in presenting time series and can help users quickly recognize an upward or downward trend in the data.
3. Heat map
    - Lack of Precise Comparison: Heat maps indicate the magnitude of values through color shades, but when it comes to specific ratings and box office of different movies, it may be difficult to make precise comparisons using heat maps because the color shades are not as intuitive as the numbers and sizes (e.g., point sizes for scatter plots).
    - Difficulty in presenting multi-dimensional information: Heat maps are better suited to presenting two-dimensional data matrices and are not suitable for presenting three-dimensional or more dimensional information. While Scatter Chart and Bubble Chart can present multiple dimensions of data at the same time through position, size, and color, and can better analyze the relationship between multiple features such as ratings, box office, and budget.

The currently selected chart types are more balanced in terms of displaying multi-dimensional information, analyzing trend changes and enhancing the user interaction experience, which can provide users with a better experience.

- Multi-dimensional display combined with trend analysis: The current selection of Scatter Chart, Bubble Chart and other methods can show the relationship between multiple features, and combined with Horizontal Chart to analyze the time trend, which creates a more comprehensive analysis perspective.
- Easy to Understand and High Information Density: Your choice of visualization methods such as tree diagrams and map visualizations are high in information density and easy to understand, demonstrating differences across a wider range of categories and regions in a limited space.
- Highly Interactive: Using Tableau for visual analytics allows you to enhance the user experience with interactive features such as filtering and hover prompts, which, combined with visualizations such as maps and bubble charts, help users better explore the data.

== Shortcomings and reflections

During the visualization and analysis process, despite using Tableau and combining the cleaned two CSV datasets for exhaustive analysis and presentation, there were still some visions that could not be realized due to the limitations of the data and the tool itself. The following are some of the shortcomings and reflections from the project:

1. Limitations of data sources and data quality
    - Shortcomings: The two CSV datasets used in the project contain a wealth of information, but there is missing or incomplete data on some key features (e.g., social media influence, audience sentiment analysis, region-specific box office, etc.). For example, some movies have incomplete data on budgets, box office revenues, ratings, etc., resulting in some data points that cannot be effectively incorporated into the analysis model when analyzing the relationship between movie production budgets and box office revenues.
    - Reflection and Improvement: If data from more sources (e.g., IMDb, Rotten Tomatoes, The Numbers, and other websites) can be obtained and more detailed information such as social media comments and changes in audience ratings can be included, we can further refine the analysis to explore the dynamic relationship between audience word-of-mouth and movie box office. In addition, in the future, we can consider using data-completion methods (e.g., predictive models for machine learning) to speculate on missing data and improve the completeness of the analysis.
2. A dynamic analysis of movie ratings and word-of-mouth communication
    - Shortcomings: Due to the lack of time-series data on the changes in audience ratings in the dataset, we fail to show the dynamic trends of ratings and word-of-mouth (WOM) dissemination during the movie's release. For example, some movies may have significant changes in ratings for a period of time after release due to word-of-mouth effects, but due to the lack of relevant data, we can only analyze the overall distribution of ratings and fail to dig deeper into the factors behind these changes.
    - Reflection and Improvement: If we can obtain time-series data of audience ratings (e.g., daily rating changes, social media heat, etc.), we can construct visual charts of dynamic rating changes (e.g., time-series heat maps) and analyze the correlation between rating changes and box office trends. This can better reveal the performance of the movie at different stages in the early and late stages of its release.
3. Analysis of box office performance and regional variations in global markets
    - Shortcomings: When analyzing the global box office performance, there is a lack of specific regional box office data, resulting in that we can only show the total box office of a movie and the basic comparison of domestic and international box office based on macro data, but cannot further break it down to analyze the box office of specific countries or regions. For example, for some movies, they perform better in the North American market, but may be cold in the Asian market. Due to the lack of detailed regional box office data in the data, we are unable to analyze these phenomena in depth.
    - Reflection and Improvement: If we can get more detailed regional box office data (e.g., box office performance of China, Japan, and European countries), we can use map visualization combined with bubble charts or color gradient charts to show the distribution of box office in different countries or regions more clearly, and help to identify the differences in box office in the global market.
4. An analysis of the relationship between social media and movie box office
    - Shortcomings: Our dataset contains some social media metrics (e.g., number of Facebook likes of directors and actors), but fails to include broader social media data (e.g., Twitter discussions, Instagram followers, Google search trends, etc.). As a result, it fails to analyze in depth the relationship between the level of movie discussion and topic buzz on social media and actual box office performance.
    - Reflection and Improvement: In the future analysis, we can consider introducing social media APIs, such as data from Twitter, Reddit and Instagram, to analyze the change of the heat of movie topics on social media, and conduct a correlation analysis in combination with box office data. This can show the synchronization of social media discussion volume and box office changes through time series charts, revealing the effect of movie marketing and word-of-mouth communication.
5. Lack of visualization of film mood and critical analysis
    - Shortcomings: Due to the lack of specific user comments and movie review texts in the dataset, we failed to perform Sentiment Analysis (Sentiment Analysis) and could not show the audience's specific emotional feedback on the movie. For example, when analyzing movie ratings, we can only look at the total score, and cannot further analyze the audience's evaluation of specific dimensions such as plot, special effects, and actors' performances.
    - Reflection and Improvement: If we have access to user review data in the future, we can use Natural Language Processing (NLP) technology to perform sentiment analysis and use sentiment time-series graphs or sentiment cloud maps to show the audience's sentiment trends and main concerns. This kind of analysis can help us understand the specific reasons behind the ratings and provide more detailed insights into audience feedback.
6. Limitations of Tableau Tools
    - Shortcomings: Tableau, while powerful, is relatively limited when it comes to performing complex statistical analyses and model building. For example, Tableau is not as flexible as programming tools such as Python or R in dealing with non-linear regression models or building advanced machine learning models. As a result, our analysis was largely limited to basic statistical and visualization analysis, and we were not able to delve into complex predictive model modeling.
    - Reflection and Improvement: Consider building predictive models (e.g., box office prediction, rating prediction, etc.) in Python or R, and then importing the results into Tableau for visualization and presentation. This can make full use of Tableau's interactive features, while combining the powerful analytical capabilities of programming tools to improve the depth and accuracy of the overall analysis.

= Contribution

|  | ZHANG Yanfeng | WAN Dingkang  | LI Yinghua | ZHANG Hongyi | HAO Xinyu  |
| --- | --- | --- | --- | --- | --- |
| Proposal |  |  | ✅ | ✅ |  |
| Data Collection |  |  |  |  |  |
| Data Preprocessing | ✅ | ✅ |  |  |  |
| Visualization and Analysis |  |  |  |  |  |
| Final Report |  |  | ✅ | ✅ |  |
| Presentation |  |  |  |  | ✅ |

= References