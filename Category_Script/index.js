const puppeteer = require('puppeteer');
const fs = require('fs');

async function scrapeZoomMarketplace() {
  let browser; // Declare browser variable here
  try {
    browser = await puppeteer.launch({
      headless: "new"
    });
    const page = await browser.newPage();
    const allApps = {};  // Store apps by category

    // Define categories with their corresponding link keywords and display names
    const categories = {
      'Analytics': 'analytics',
      'Broadcasting & Streaming': 'broadcasting-streaming',
      'Business System Integrator': 'business-system-integrator',
      'CRM': 'crm',
      'Carrier Provider Exchange': 'carrier-provider-exchange',
      'Collaboration': 'team-collaborations',
      'Customer Service': 'customer-service',
      'E-Commerce': 'eCommerce',
      'Education': 'education',
      'Event Management': 'eventmanagement',
      'Financial Services': 'financialServices',
      'Games': 'games',
      'Government': 'government',
      'Health & Wellness': 'health-wellness',
      'Healthcare': 'health-care',
      'Human Resources': 'human-resources',
      'Learning & Development': 'learning-development',
      'Marketing': 'marketing',
      'Note Taking': 'note-taking',
      'Presentations': 'presentations',
      'Productivity': 'productivity',
      'Project Management': 'project-management',
      'Recordings': 'recording-transcriptions',
      'Sales': 'sales-automation',
      'Scheduling': 'scheduling-calendar',
      'Security & Compliance': 'content-and-compliance',
      'Social Activities': 'social-activities',
      'Surveys & Polls': 'surveys-polls',
      'Transcription & Translation': 'transcription-translation',
      'Virtual Backgrounds & Scenes': 'virtual-backgrounds-scenes',
      'Whiteboards': 'whiteboards',
      'Workflow Automation': 'workflow-automation'
    };

    for (const [categoryName, linkKeyword] of Object.entries(categories)) {
      console.log(`Processing category: ${categoryName}`);
      const categoryApps = [];

      for (let pageNum = 1; pageNum <= 30; pageNum++) {
        const url = `https://marketplace.zoom.us/apps?category=${linkKeyword}&page=${pageNum}`;
        
        console.log(`Scraping page ${pageNum}...`);
        
        let attempts = 0; // Initialize attempts counter
        const maxAttempts = 10; // Set maximum attempts

        while (attempts < maxAttempts) {
          try {
            await page.goto(url, {
              waitUntil: 'networkidle0',
              timeout: 10000
            });
            break; // Exit loop if successful
          } catch (error) {
            attempts++;
            console.error(`Attempt ${attempts} failed: ${error.message}`);
            if (attempts === maxAttempts) {
              console.log(`Failed to load page ${pageNum} after ${maxAttempts} attempts.`);
              throw error; // Rethrow error after max attempts
            }
            console.log(`Retrying page ${pageNum}...`);
            await new Promise(resolve => setTimeout(resolve, 5000)); // Wait before retrying
          }
        }

        const namesOnPage = await page.evaluate(() => {
          const elements = document.querySelectorAll('.css-1kt17r2');
          return Array.from(elements).map(element => element.textContent.trim());
        });

        if (namesOnPage.length === 0) {
          console.log(`No more apps found after page ${pageNum-1} for category ${categoryName}`);
          break;
        }

        categoryApps.push(...namesOnPage);
        
        // Fixed delay between requests
        await new Promise(resolve => setTimeout(resolve, 1000));
      }

      allApps[categoryName] = categoryApps;
    }

    fs.writeFileSync('zoom_apps_new.json', JSON.stringify(allApps, null, 2));
    console.log(`Successfully scraped apps from ${Object.keys(allApps).length} categories to zoom_apps_new.json`);

  } catch (error) {
    console.error('An error occurred:', error);
  } finally {
    // Ensure browser closes even if there's an error
    if (browser) {
      await browser.close();
    }
  }
}

// Start the scraping process
scrapeZoomMarketplace();