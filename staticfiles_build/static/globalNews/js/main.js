const share_links__BLOCK = document.querySelector(".share_links--BLOCK");
(function (){
    
    const shareArticleOverlay__BLOCK = document.querySelector('.share_overlay--BLOCK');
    const share_links__BLOCK = document.querySelector(".share_links--BLOCK");
    // Share article on social media -- SECTION
    const shareArticle__BTNS = document.querySelectorAll(".share_news_article_btn--BLOCK");
    
    const close_shareArticle__BTN = document.querySelector(".close_share_overlay--BTN")
    
    const twitterShare__BTN = document.querySelector(".share_in_twitter--BTN");
    const facebookShare__BTN = document.querySelector(".share_in_facebook--BTN");
    const copy_articleUrl__BTN = document.querySelector(".copy_url--BTN");
    
    shareArticle__BTNS.forEach(shareArticle__BTN => {
        shareArticle__BTN?.addEventListener("click" ,() => {
            const shareArticleOverlay__STATUS = shareArticleOverlay__BLOCK.dataset.visible;
            if(shareArticleOverlay__STATUS === "true"){
                shareArticleOverlay__BLOCK.dataset.visible = false;
            } else {
                shareArticleOverlay__BLOCK.dataset.visible = true;

                const articleSource = shareArticle__BTN.querySelector("input[name=articleSource]")?.value;
                const articleTitle = shareArticle__BTN.querySelector("input[name=articleTitle]")?.value;
                const articleUrl = shareArticle__BTN.querySelector("input[name=articleUrl]")?.value;

                const articleSource__EL = shareArticleOverlay__BLOCK?.querySelector(".article_source--EL");
                const articleTitle__EL = shareArticleOverlay__BLOCK?.querySelector("h6");

                articleSource__EL.innerText = articleSource;
                articleTitle__EL.innerText = articleTitle;
                
                twitterShare__BTN?.addEventListener("click", () => {
                    const twitter_share_url = `http://twitter.com/intent/tweet`;
                    const twitter_share_query = `?text=${articleTitle}&url=${articleUrl}`;

                    window.open(`${twitter_share_url}${twitter_share_query}`)
                })

                facebookShare__BTN?.addEventListener("click", ()=> {
                    const facebook_share_url = `https://www.facebook.com/sharer/sharer.php`;
                    const facebook_share_query = `?u=${articleUrl}`;

                    window.open(`${facebook_share_url}${facebook_share_query}`)
                })

                copy_articleUrl__BTN?.addEventListener("click", () => {
                    navigator.clipboard.writeText(articleUrl);
                })

                // ---- Close Sharing state
                shareArticleOverlay__BLOCK?.addEventListener("click", evt => {
                    if(shareArticleOverlay__BLOCK && shareArticleOverlay__BLOCK?.dataset.visible === "true" && !share_links__BLOCK.contains(evt.target)){
                        shareArticleOverlay__BLOCK.dataset.visible = "false"
                    }
                })
                // ---------------------
            }
        })
    })
    
    // Close article share block
    close_shareArticle__BTN?.addEventListener("click", ()=>shareArticleOverlay__BLOCK.dataset.visible = false)
})()


////////////////////////////////////////////////////////////////////////////

// Navbar User Profile Block -- SECTION
const nav_user_profile__BLOCK = document.querySelector(".loggedIn_user_links--BLOCK");
const nav_user_profile__BTN = document.querySelector(".loggedIn_user_profile--BTN");
const nav_user_profile__DROPDOWN = document.querySelector(".loggedIn_user_links--DROPDOWN");

nav_user_profile__BTN?.addEventListener("click", () => {
    const profile_dropdown_visibility_attr_value = nav_user_profile__DROPDOWN.dataset.visible;

    if(profile_dropdown_visibility_attr_value == "false"){
        nav_user_profile__DROPDOWN.dataset.visible = true;
    } else {
        nav_user_profile__DROPDOWN.dataset.visible = false;
    }
})
////////////////////////////////////////////////////////////////////////////


// user account password setting -- SECTION
const expand_user_password_fiels__BTN = document.querySelector(".change_user_password--BTN");
const expand_user_password_fiels__CONTAINER = document.querySelector(".change_user_password_fields--CONTAINER");

expand_user_password_fiels__BTN?.addEventListener("click", evt => {
    let user_password_fiels__CONTAINER__STATE = expand_user_password_fiels__CONTAINER?.dataset.expanded;

    console.log("click click click click ");
    console.log(user_password_fiels__CONTAINER__STATE);

    if(user_password_fiels__CONTAINER__STATE == "false"){
        expand_user_password_fiels__CONTAINER?.setAttribute("data-expanded", true);
        expand_user_password_fiels__BTN.remove();
    } else {
        expand_user_password_fiels__CONTAINER?.setAttribute("data-expanded", false);
    }
})
////////////////////////////////////////////////////////////////////////////


// location search -- SECTION
const search_country__BLOCK = document.querySelector(".location_selection_formInput--BLOCK");
const search_country__FORM = document.querySelector(".location_selection--FORM");
const search_country__INPUT = document.querySelector(".search_country--INPUT");
const countries__CONTAINER = document.querySelector(".available_countries_options--CONTAINER");

countries__CONTAINER?.addEventListener("click", evt => {
    const choosenCountry__EL = evt.target.innerText;

    if (choosenCountry__EL){
        search_country__INPUT.value = choosenCountry__EL;
        search_country__BLOCK.setAttribute("aria-expanded", false)

        search_country__FORM.submit()
    }
})

const loadAvailableCountries__HANDLER = (countries_search_result) => {
    if(countries_search_result){
        countries__CONTAINER.innerHTML = "";
        
        fetch("/availableCountries")
        .then(res => res.json())
        .then(data => {
            const countries = data.filter(country => country.toLowerCase().includes(countries_search_result.toLowerCase()));

            
            if(countries.length){
                search_country__BLOCK.setAttribute("aria-expanded", true)
                let country_selection_El__HEIGHT = 0;

                countries.forEach(country => {
                    const country_selection__EL = document.createElement("span");
                    
                    country_selection__EL.className = "available_countries--OPTION mid__FONTSIZE";
                    country_selection__EL.innerText = country;
    
                    countries__CONTAINER.appendChild(country_selection__EL);

                    country_selection_El__HEIGHT = country_selection__EL.offsetHeight;
                });

                if(countries.length > 10){
                    countries__CONTAINER.style.height = `${country_selection_El__HEIGHT * 10}px`
                } else {
                    countries__CONTAINER.style.height = "auto";
                }
            } else {
                search_country__BLOCK.setAttribute("aria-expanded", false)
            }
        })
    } else {
        search_country__BLOCK.setAttribute("aria-expanded", false)
    }
}

search_country__INPUT?.addEventListener("focus", evt => {
    let countries_search_result = evt.currentTarget.value;
    loadAvailableCountries__HANDLER(countries_search_result)
})

search_country__INPUT?.addEventListener("keyup", evt => {
    let countries_search_result = evt.currentTarget.value;
    
    loadAvailableCountries__HANDLER(countries_search_result)
})
////////////////////////////////////////////////////////////////////////////

// Save and Unsave News Article form full article page -- SECTION

const save_newsArticle__FORM = document.querySelector("#save_newsArticle--FORM");
save_newsArticle__FORM?.addEventListener("submit", evt => {
    evt.preventDefault();

    const csrf_token = evt.target.csrfmiddlewaretoken.value;

    const newsArticle_title = evt.target.title.value;
    const newsArticle_description = evt.target.description.value;
    const newsArticle_articleUrl = evt.target.articleUrl.value;
    const newsArticle_thumbnail = evt.target.thumbnail.value;
    let newsArticle_PublishmentDate = evt.target.PublishmentDate.value;
    const newsArticle_source = evt.target.source.value;

    if(newsArticle_PublishmentDate.includes(",")){
        const editedPublishDate__STR = newsArticle_PublishmentDate.split(",").slice(0, -1).join("")

        const editedPublishDate = new Date(editedPublishDate__STR);
        newsArticle_PublishmentDate = editedPublishDate.toString("yyyy-MM-dd HH:mm:ss")
    }

    const data = {
        title: newsArticle_title,
        description: newsArticle_description,
        articleUrl: newsArticle_articleUrl,
        thumbnail: newsArticle_thumbnail,
        PublishmentDate: newsArticle_PublishmentDate,
        source: newsArticle_source,
    }

    console.log(data);

    fetch("/save_newsArticle", {
        method:"POST",
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrf_token
        },
        mode: 'same-origin',
        body:JSON.stringify(data)
    })
    .then(res => res.json())
    .then(data => {
        if(data.status == "success"){
            if(data.type == "saved"){
                save_newsArticle__FORM.dataset.saved = true;
            } else {
                save_newsArticle__FORM.dataset.saved = false;
            }
        }
    })
})

////////////////////////////////////////////////////////////////////////////

// Save Article -- SECTION
const news_article__CARDS = document.querySelectorAll('.news_article--CARD');
news_article__CARDS?.forEach(news_article__CARD => {
    const save_article__FORM = news_article__CARD?.querySelector("form");

    save_article__FORM?.addEventListener("submit", evt => {
        evt.preventDefault();

        const save_article_btn__BLOCK = evt.currentTarget.querySelector(".bookmark_news_article_btn--BLOCK");
        const save_article_btn__BANNER = save_article_btn__BLOCK.querySelector(".news_article_cta_hover--BANNER");

        const csrf_token = evt.target.csrfmiddlewaretoken.value;

        const newsArticle_title = evt.target.title.value;
        const newsArticle_description = evt.target.description.value;
        const newsArticle_articleUrl = evt.target.articleUrl.value;
        const newsArticle_thumbnail = evt.target.thumbnail.value;
        const newsArticle_PublishmentDate = evt.target.PublishmentDate.value;
        const newsArticle_source = evt.target.source.value;

        const data = {
            title: newsArticle_title,
            description: newsArticle_description,
            articleUrl: newsArticle_articleUrl,
            thumbnail: newsArticle_thumbnail,
            PublishmentDate: newsArticle_PublishmentDate,
            source: newsArticle_source,
        }

        fetch("/save_newsArticle", {
            method:"POST",
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrf_token
            },
            mode: 'same-origin',
            body:JSON.stringify(data)
        })
        .then(res => res.json())
        .then(data => {
            if(data.status == "success"){
                if(data.type == "saved"){
                    save_article_btn__BLOCK.dataset.saved = true;
                    save_article_btn__BANNER.innerText = "remove from save list";
                } else {
                    save_article_btn__BLOCK.dataset.saved = false;
                    save_article_btn__BANNER.innerText = "save for later";
                }
            }
        })
    })
})
////////////////////////////////////////////////////////////////////////////


// Unsave News Article -- SECTION
const saved_news_articles__BLOCK = document.querySelector(".saved_news_articles--BLOCK");
const saved_news_articles__CARDS = saved_news_articles__BLOCK?.querySelectorAll(".news--CARD");

saved_news_articles__CARDS?.forEach(saved_news_articles__CARD => {
    const saved_news_articles__CARD_FORM = saved_news_articles__CARD.querySelector(".news_article--CTAs form");

    saved_news_articles__CARD_FORM?.addEventListener('submit', evt => {
        evt.preventDefault();

        const csrf_token = evt.target.csrfmiddlewaretoken.value;

        const newsArticle_title = evt.target.title.value;
        const newsArticle_source = evt.target.source.value;

        const data = {
            title: newsArticle_title,
            source: newsArticle_source,
        }

        fetch("/unsaveNewsArticle", {
            method:"POST",
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrf_token
            },
            mode: 'same-origin',
            body:JSON.stringify(data)
        })
        .then(res => res.json())
        .then(data => {
            if(data.status == "success"){
                saved_news_articles__CARD.remove();
            } else {
                const unsaveArticle_error__BLOCK = saved_news_articles__BLOCK.querySelector(".unsaveArticle_error--BLOCK");
                unsaveArticle_error__BLOCK.classList.add("show_unsaveArticle_error");
            }
        })
    })
})
////////////////////////////////////////////////////////////////////////////

// FOLLOW AND UNFOLLOW A TOPIC -- SECTION 
const follow_topic__FORM = document.querySelector('.follow_topic--FORM');
follow_topic__FORM?.addEventListener("submit", evt => {
    evt.preventDefault();

    const follow_topic__BTN = evt.currentTarget.querySelector(".follow_topic--BTN");
    
    const csrf_token = evt.target.csrfmiddlewaretoken.value;
    const topicTitle = evt.target.topic_title.value;

    fetch(`/followTopic/${topicTitle}`, {
        method:"POST",
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrf_token
        },
        mode: 'same-origin'
    })
    .then(res => res.json())
    .then(data => {
        if(data.status == "success"){
            if(data.type === "follow"){
                follow_topic__BTN.dataset.followed = true;
            } else {
                follow_topic__BTN.dataset.followed = false;
            }
        } else {
            alert("Something went Wrong, Please try again later!!")
        }
    })
})
////////////////////////////////////////////////////////////////////////////

// Loading current user random topics
const user_topics__SECTION = document.querySelector(".user_topics--SECTION");

document.addEventListener("DOMContentLoaded", evt => {
    const currentUser_randomTopics__STR = evt.currentTarget.querySelector("#currentUser_random3Topics")?.value;
    const currentUser_randomTopics__LIST = currentUser_randomTopics__STR?.split(",");

    const currentUser_randomTopics__URLS_LIST = currentUser_randomTopics__LIST.map(currentUser_randomTopic => `followedTopic/${currentUser_randomTopic}`);

    Promise.all(currentUser_randomTopics__URLS_LIST.map(currentUser_randomTopic__URL=>fetch(currentUser_randomTopic__URL)))
    .then(responses => Promise.all(responses.map(res => res.json()))
    ).then(randomTopics_NewsArticles_LIST => {
        console.log(randomTopics_NewsArticles_LIST);
        randomTopics_NewsArticles_LIST.forEach(randomTopics_NewsArticle__OBJ => displayFollowedTopic_NewsArticles_Block__HANDLER(randomTopics_NewsArticle__OBJ))
    })
})
////////////////////////////////////////////////////////////////////////////

document.addEventListener("click" , evt => {
    // Close Location Search Options
    if(search_country__BLOCK && !search_country__BLOCK?.contains(evt.target)){
        search_country__BLOCK.setAttribute("aria-expanded", false)
    }
    //----------------------------------------------------------
    
    
    // Close Navbar user profile Dropdown
    if(nav_user_profile__BLOCK && !nav_user_profile__BLOCK?.contains(evt.target)){
        nav_user_profile__DROPDOWN.dataset.visible = false;
    }
    //----------------------------------------------------------
})

// GLOBAL FUNCTIONS

const displayFollowedTopic_NewsArticles_Block__HANDLER = (topicResults__OBJ) => {
    if(topicResults__OBJ.status === "success"){
        const currentUser_followedTopics__CARDSCONTAINER = user_topics__SECTION?.querySelector(".user_topics--CARDSCONTAINER");

        // FOLLOWED TOPIC ARTICLE ELEMENT CONTENT
            const currentUser_followedTopic__ARTICLE = document.createElement("article");
            currentUser_followedTopic__ARTICLE.className = "user_topic--CARD";
        //////////////////////////////////////////////////////
        
        // FOLLOWED TOPIC CARD CONTENT WRAPPER ELEMENT
            const currentUser_followedTopic__ARTICLE_CONTENT = document.createElement("div");
            currentUser_followedTopic__ARTICLE_CONTENT.className = "user_topic--CARDCONTENT";
        //////////////////////////////////////////////////////
        
        // FOLLOWED TOPIC ARTICLE CONTENT ARTICLE HEADER
            const currentUser_followedTopic__ARTICLE_HEADER = document.createElement("header");
            currentUser_followedTopic__ARTICLE_HEADER.className = "user_topic--CARDHEADER";
        
            // FOLLOWED TOPIC CARD HEADER CONTENT
                const currentUser_followedTopic__ARTICLE_HEADER_LINK = document.createElement("a");
                currentUser_followedTopic__ARTICLE_HEADER_LINK.href = `search?q=${topicResults__OBJ.topic}`;
                
                const currentUser_followedTopic__ARTICLE_HEADER_TITLE = document.createElement("h3");
                currentUser_followedTopic__ARTICLE_HEADER_TITLE.innerText = topicResults__OBJ.topic;
                currentUser_followedTopic__ARTICLE_HEADER_TITLE.className = "large__FONTSIZE";

                currentUser_followedTopic__ARTICLE_HEADER_LINK.appendChild(currentUser_followedTopic__ARTICLE_HEADER_TITLE);
            // ----------------------------------------------------------------
            currentUser_followedTopic__ARTICLE_HEADER.appendChild(currentUser_followedTopic__ARTICLE_HEADER_LINK)
        //////////////////////////////////////////////////////
        
        // FOLLOWED TOPIC NEWS ARTICLES CONTAINER
            const currentUser_followedTopic_newsArticles__CONTAINER = document.createElement("div");
            currentUser_followedTopic_newsArticles__CONTAINER.className = "user_topic_news--CONTAINER";

            topicResults__OBJ.articles.forEach(article => {
                const article_source = article.source.split(".").splice(0, article.source.split(".").length -1 ).join(" ");

                // followed topic card block
                    const article__BLOCK = document.createElement("div");
                    article__BLOCK.className = "news--CARD";
                    
                    // followed topic card link
                    const article_card__LINK = document.createElement("a");
                    article_card__LINK.target=`_blank`;
                    article_card__LINK.href=`${article.url}`;
                    article_card__LINK.className="news_card--CONTENT";

                    // followed topic card infos container
                        const followedTopic_infos__BLOCK = document.createElement("div");
                        followedTopic_infos__BLOCK.className="news_card_infos--CONTAINER";
                        // followed topic card infos -- LEFTSIDE BLOCK
                            const followedTopic_infos_leftside_infos__CONTAINER = document.createElement("div");
                            followedTopic_infos_leftside_infos__CONTAINER.className="news_card--LEFTSIDE";

                            // followed topic card -- HEADER
                                const followed_topic_card__HEADER = document.createElement("div");
                                followed_topic_card__HEADER.className = "article_aditional_infos--CONTAINER";
                                    
                                    // followed topic card header -- CONTENT
                                        // followed topic article -- SINCE PUBLISHMENT TIME - BLOCK
                                            const followedTopic_article_sincePublishmentTime__BLOCK = document.createElement("div");
                                            followedTopic_article_sincePublishmentTime__BLOCK.className="news_card_sincePublishmentTime--BLOCK";
                                            
                                            // followed topic article -- SINCE PUBLISHMENT TIME - ICON CONTAINER
                                                const sincePublishmentTime_icon__CONTAINER = document.createElement("span");
                                                sincePublishmentTime_icon__CONTAINER.className = "news_card_sincePublishmentTime--WRAPPER";
                                                // followed topic article -- SINCE PUBLISHMENT TIME - ICON
                                                    const sincePublishmentTime__ICON = document.createElement("img");
                                                    sincePublishmentTime__ICON.src = "../assets/icons/clock.png";
                                                // --------------------------------------------------------
                                                sincePublishmentTime_icon__CONTAINER.appendChild(sincePublishmentTime__ICON);
                                            // ------------------------------------------------------------
                                            const article_sincePublishmentTime__EL = document.createElement("span");
                                            article_sincePublishmentTime__EL.className = "news_card_sincePublishmentTime--EL small-mid__FONTSIZE";
                                            article_sincePublishmentTime__EL.innerText = article.sincePubTime;

                                            followedTopic_article_sincePublishmentTime__BLOCK.appendChild(sincePublishmentTime_icon__CONTAINER)
                                            followedTopic_article_sincePublishmentTime__BLOCK.appendChild(article_sincePublishmentTime__EL)
                                        // ----------------------------------------------------------------
                                        // followed topic source -- ELEMENT
                                            const leftside_card_source__EL = document.createElement("span")
                                            leftside_card_source__EL.className="small-mid__FONTSIZE news_article_source--EL";

                                            leftside_card_source__EL.innerText = article_source;
                                        // ----------------------------------------------------------------
                                    // ---------------------------------------------
                                followed_topic_card__HEADER.appendChild(followedTopic_article_sincePublishmentTime__BLOCK)
                                followed_topic_card__HEADER.appendChild(leftside_card_source__EL)
                                
                            // --------------------------------------------------
                            const leftside_card_title__EL = document.createElement("h4")
                            leftside_card_title__EL.className="mid__FONTSIZE";
                            leftside_card_title__EL.innerText = article.title;

                            followedTopic_infos_leftside_infos__CONTAINER.appendChild(followed_topic_card__HEADER)
                            followedTopic_infos_leftside_infos__CONTAINER.appendChild(leftside_card_title__EL)
                        // --------------------------------------------------

                        // followed topic card thumbnail -- FIGURE
                            const followedTopic_figure__EL = document.createElement("figure");
                            followedTopic_figure__EL.className="news_image--CONTAINER";

                            // followed topic card thumbnail -- IMG
                                const followedTopic_figure_IMG = document.createElement("img");
                                if(article.image_url){
                                    followedTopic_figure_IMG.src = article.image_url;
                                    followedTopic_figure_IMG.alt = article.title;
                                } else {
                                    followedTopic_figure_IMG.src = "../assets/background/default_news_thumbnail 2.png";
                                    followedTopic_figure_IMG.alt = "article's thumbnail is not available.";
                                }
                            // --------------------------------------------
                            followedTopic_figure__EL.appendChild(followedTopic_figure_IMG);
                        // --------------------------------------------------
                        followedTopic_infos__BLOCK.appendChild(followedTopic_infos_leftside_infos__CONTAINER)
                        followedTopic_infos__BLOCK.appendChild(followedTopic_figure__EL)
                    // ----------------------------------------------------------------
                    
                    article_card__LINK.appendChild(followedTopic_infos__BLOCK)

                    article__BLOCK.appendChild(article_card__LINK)
                // -------------------------------------------------------------
                currentUser_followedTopic_newsArticles__CONTAINER.appendChild(article__BLOCK);
            })
        //////////////////////////////////////////////////////

        currentUser_followedTopic__ARTICLE_CONTENT.appendChild(currentUser_followedTopic__ARTICLE_HEADER)
        currentUser_followedTopic__ARTICLE_CONTENT.appendChild(currentUser_followedTopic_newsArticles__CONTAINER)
        
        currentUser_followedTopic__ARTICLE.appendChild(currentUser_followedTopic__ARTICLE_CONTENT)
    
        currentUser_followedTopics__CARDSCONTAINER.appendChild(currentUser_followedTopic__ARTICLE)
    }
}