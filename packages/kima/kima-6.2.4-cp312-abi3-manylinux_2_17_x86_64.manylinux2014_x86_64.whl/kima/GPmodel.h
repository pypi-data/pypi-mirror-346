#pragma once

#include <vector>
#include <memory>
#include <array>
#include "DNest4.h"
#include "Data.h"
#include "ConditionalPrior.h"
#include "utils.h"
#include "kepler.h"
#include "AMDstability.h"
#include "default_priors.h"
#include "GP.h"

#include <Eigen/Core>
#include <Eigen/Dense>
#include <Eigen/Cholesky>

using namespace std;
using namespace DNest4;

// for nanobind
#include <nanobind/nanobind.h>
namespace nb = nanobind;
using namespace nb::literals;
#include "nb_shared.h"

class  GPmodel
{
    protected:
        /// Fix the number of planets? (by default, yes)
        bool fix {true};

        /// Maximum number of planets (by default 1)
        int npmax {1};

        /// whether the model includes a polynomial trend
        bool trend {false};
        /// degree of the polynomial trend
        int degree {0};   

        /// stellar mass (in units of Msun)
        double star_mass = 1.0;

        /// whether to enforce AMD-stability
        bool enforce_stability = false;

        /// include in the model linear correlations with indicators
        bool indicator_correlations = false;
        /// whether to consider a (periodic) GP kernel for a magnetic cycle
        bool magnetic_cycle_kernel = false;

        RVData data;

    private:
        Eigen::VectorXd v_t, v_dt;  // store t and dt for SPLEAF kernels
        Eigen::VectorXd sig_copy;  // copy of RV uncertainties for the GP covariance


        DNest4::RJObject<KeplerianConditionalPrior> planets =
            DNest4::RJObject<KeplerianConditionalPrior>(5, npmax, fix, KeplerianConditionalPrior());

        double background;

        std::vector<double> offsets; // between instruments
            //   std::vector<double>(0, data.number_instruments - 1);
        std::vector<double> jitters; // for each instrument
            //   std::vector<double>(data.number_instruments);

        std::vector<double> betas; // "slopes" for each indicator
            //   std::vector<double>(data.number_indicators);

        double slope, quadr=0.0, cubic=0.0;
        double extra_sigma;
        double nu;

        // Parameters for the known object, if set
        // double KO_P, KO_K, KO_e, KO_phi, KO_w;
        std::vector<double> KO_P;
        std::vector<double> KO_K;
        std::vector<double> KO_e;
        std::vector<double> KO_phi;
        std::vector<double> KO_w;

        // Parameters for the transiting planet, if set
        std::vector<double> TR_P;
        std::vector<double> TR_K;
        std::vector<double> TR_e;
        std::vector<double> TR_Tc;
        std::vector<double> TR_w;

        double eta1, eta2, eta3, eta4;
        double log_eta1, log_eta2, log_eta3, log_eta4;
        bool _eta2_larger_eta3 = false;
        double _eta2_larger_eta3_factor = 1.0;

        double Q;
        double eta5, eta6, eta7;
        double log_eta5, log_eta6, log_eta7;

        // The signal
        std::vector<double> mu; // = std::vector<double>(data.N());
        // The covariance matrix for the data
        Eigen::MatrixXd C; // {data.N(), data.N()};

        void calculate_mu();
        void calculate_C();
        void add_known_object();
        void remove_known_object();
        void add_transiting_planet();
        void remove_transiting_planet();

        int is_stable() const;

        unsigned int staleness;


    public:
        GPmodel() {};
        GPmodel(bool fix, int npmax, RVData& data) : fix(fix), npmax(npmax), data(data) {
            initialize_from_data(data);
        };

        void initialize_from_data(RVData& data);

        using distribution = std::shared_ptr<DNest4::ContinuousDistribution>;
        // priors for parameters *not* belonging to the planets
        /// Prior for the systemic velocity.
        distribution Cprior;
        /// Prior for the extra white noise (jitter).
        distribution Jprior;
        /// Prior for the slope
        distribution slope_prior;
        /// Prior for the quadratic coefficient of the trend
        distribution quadr_prior;
        /// Prior for the cubic coefficient of the trend
        distribution cubic_prior;
        /// (Common) prior for the between-instruments offsets.
        distribution offsets_prior;
        /// Individual priors for the between-instruments offsets.
        std::vector<distribution> individual_offset_prior; // { (size_t) data.number_instruments - 1 };
        /// (Common) prior for the activity indicator coefficients
        distribution beta_prior;

        /* KO mode! */

        /// include (better) known extra Keplerian curve(s)?
        bool known_object {false};
        bool get_known_object() { return known_object; }

        /// how many known objects
        size_t n_known_object {0};
        size_t get_n_known_object() { return n_known_object; }

        void set_known_object(size_t known_object);

        /// Prior for the KO orbital period(s)
        std::vector<distribution> KO_Pprior;
        /// Prior for the KO semi-amplitude(s)
        std::vector<distribution> KO_Kprior;
        /// Prior for the KO eccentricity(ies)
        std::vector<distribution> KO_eprior;
        /// Prior for the KO mean anomaly(ies)
        std::vector<distribution> KO_phiprior;
        /// Prior for the KO argument(s) of pericenter
        std::vector<distribution> KO_wprior;

        /* Transiting planets! */

        /// include known extra Keplerian curve(s) for transiting planet(s)?
        bool transiting_planet {false};
        bool get_transiting_planet() { return transiting_planet; }

        /// how many known objects
        size_t n_transiting_planet {0};
        size_t get_n_transiting_planet() { return n_transiting_planet; }

        void set_transiting_planet(size_t transiting_planet);

        /// Prior for the TR orbital period(s)
        std::vector<distribution> TR_Pprior;
        /// Prior for the TR semi-amplitude(s)
        std::vector<distribution> TR_Kprior;
        /// Prior for the TR eccentricity(ies)
        std::vector<distribution> TR_eprior;
        /// Prior for the TR time(s) of transit
        std::vector<distribution> TR_Tcprior;
        /// Prior for the TR argument(s) of pericenter
        std::vector<distribution> TR_wprior;


        KernelType kernel {qp};

        // priors for the GP hyperparameters
        /// Prior for $\eta_1$, the GP "amplitude"
        distribution eta1_prior;
        /// Prior for $\eta_2$, the GP correlation timescale
        distribution eta2_prior;
        /// Prior for $\eta_3$, the GP period
        distribution eta3_prior;
        /// Prior for $\eta_4$, the recurrence timescale
        distribution eta4_prior;
        /// Prior for $Q$, the quality factor in a SHO kernel
        distribution Q_prior;

        /// Prior for $\eta_5$, the "amplitude" of the magnetic cycle kernel
        distribution eta5_prior;
        /// Prior for $\eta_6$, the period of the magnetic cycle kernel
        distribution eta6_prior;
        /// Prior for $\eta_7$, the recurrence timescale of the magnetic cycle kernel
        distribution eta7_prior;

        /// Constrain $\eta_2$ to be larger than factor * $\eta_3$
        void eta2_larger_eta3(double factor=1.0);

        // /// @brief an alias for RVData::get_instance()
        // static RVData& get_data() { return RVData::get_instance(); }

        KeplerianConditionalPrior* get_conditional_prior() {
            return planets.get_conditional_prior();
        }
        void set_conditional_prior(const KeplerianConditionalPrior &conditional) {
            planets = DNest4::RJObject<KeplerianConditionalPrior>(5, npmax, fix, conditional);
        }

        /// @brief Generate a point from the prior.
        void from_prior(DNest4::RNG& rng);

        /// @brief Set the default priors
        void setPriors();

        /// @brief Save the setup of this model
        void save_setup();

        /// @brief Do Metropolis-Hastings proposals.
        double perturb(DNest4::RNG& rng);

        /// @brief log-likelihood function
        double log_likelihood() const;

        // Print parameters to stream
        void print(std::ostream& out) const;

        // Return string with column information
        std::string description() const;

        // Directory where the model runs
        std::string directory = "";

};

